"""Provide support for retrieving document list and documents from
the ERCOT public and private APIs"""

from pathlib import Path
import requests
from requests.exceptions import HTTPError, ReadTimeout, SSLError
from loguru import logger
from ..connector import Connector
from ..utils import get_filename_from_headers


def save_to_path(contents, path, filename) -> Path:
    """Write the contents of a downloaded file (binary) to
    the given path/filename."""

    path = Path(path)
    outpath = path / filename

    if outpath.exists():
        logger.warning(f'Ovewriting file: {filename}')
    elif path.exists() is False:
        path.mkdir(parents=True, exist_ok=True)

    with open(outpath, 'wb') as f:
        f.write(contents)

    logger.success(f'Saved {filename} to {path}')
    return outpath


class ERCOTConnector(Connector):

    def __init__(self):
        self.session = requests.Session()

    def fetch(self, url):

        logger.info(f"Fetching: {url}")

        response = None

        if self.token is None:
            logger.warning('No token - Cannot fetch respource without token')
            return response

        try:
            response = self.session.get(
                url=url,
                timeout=10
            )
            response.raise_for_status()

        except HTTPError as err:
            logger.error(err)
            logger.error(response.json().get('message', 'Unspecified Message'))

        except SSLError as err:
            logger.error(err)
        except ReadTimeout as err:
            logger.error(err)

        try:
            if response.json().get('ResponseFaultList'):
                for fault in response.json().get('ResponseFaultList'):
                    logger.error(fault['ResponseFault']['FaultDescription'])
        except requests.exceptions.JSONDecodeError:
            # Not a JSON document.
            pass

        return response

    def fetch_url(self, url, save_path):
        """Fetch the document resource (.zip/.csv/.???) and save it to the
        save_path folder.  Save the file with the same filename returned
        in the response header."""

        response = self.fetch(url)
        fname = get_filename_from_headers(response.headers)
        if fname is None:
            print('No document received.')
            logger.error("Expected file has no filename.")
            raise FileNotFoundError
        return save_to_path(response.content, save_path, fname)


class ERCOTPrivateConnector(ERCOTConnector):

    required = ['cert']

    def __init__(self):

        self.cert = ()
        super().__init__()

    def fetch_doc(self, document, save_path):
        """Convert the document id into the URL for fetching the resource."""
        url = f"https://mis.ercot.com/misdownload/servlets/mirDownload?doclookupId={document[0]}"
        return self.fetch_url(url, save_path)

    def fetch_listing(self, report_type_id, page=None):
        """Fetch download list for requested report. Return a list of
        document tuples (docid, date, constructed_name) as well as any metadata
        returned by the report. Include the metadata from the response if it is
        included."""

        url = f"https://mis.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId={report_type_id}"

        if page is not None:
            assert page > 0, 'page must be greater than 0'
            url += f"?page={page}"

        results = []
        response = self.fetch(url)

        if response.json().get('ListDocsByRptTypeRes'):
            for document in [x['Document'] for x in response.json()['ListDocsByRptTypeRes']['DocumentList']]:
                results.append([
                    document['DocID'],
                    document['PublishDate'],
                    document['ConstructedName']
                ])
        else:
            logger.error("Invalid JSON response.")

        return results, response.json().get('_meta')

    def get_token(self):
        """Just verify that we have a supplied certificate for now.
        Kick any settings into the session at this point.
        """

        cert = Path(self.cert[0])
        # Verify that the cert and key file exist.
        if cert.exists() is False:
            logger.error("Supplied certificate path does not exist.")
            return None

        key = Path(self.cert[1])
        if self.cert[1].exists() is False:
            logger.error("Supplied key path does not exist.")
            return None

        # Just in case they passed in string values instead of path objects.
        self.cert = (cert, key)
        self.session.cert = self.cert

        # We'll let the actual call determine whether they work or not.
        return 'working-ish'


class ERCOTPublicConnector(ERCOTConnector):

    required = ['username', 'password', 'primary_key', 'auth_url']

    def __init__(self):
        self.username = None
        self.password = None
        self.primary_key = None
        self.auth_url = None
        super().__init__()

    def fetch_emil_doc(self, emil_id, doc_id, save_path):
        """Generate URL and fetch the attached document."""
        url = f"https://api.ercot.com/api/public-reports/archive/{emil_id}?download={doc_id}"
        return self.fetch_url(url, save_path)

    def fetch_listing(self, emil_id, page=None):
        """Fetch download list for requested report."""

        url = f"https://api.ercot.com/api/public-reports/archive/{emil_id}"

        if page is not None:
            assert page > 0, 'page must be greater than 0'
            url += f"?page={page}"

        results = []
        response = self.fetch(url)

        if response.json().get('archives'):

            if response.json().get('archives'):
                for row in response.json().get('archives'):
                    results.append([
                        row['docId'],
                        row['postDatetime'],
                        row['_links']['endpoint']['href']
                    ])

        # Get the meta results from the call.  Record count, page count, etc.
        return results, response.json().get('_meta')

    def get_token(self):
        """Get the tokenId from the ERCOT Public API service.
        Kick any settings into the session at this point.
        """

        logger.info("Generating and Submitting Token Request for %s." % self.username)
        url = self.auth_url.format(username=self.username, password=self.password)

        try:
            response = requests.post(url=url, timeout=30)
            response.raise_for_status()
            token = response.json().get("access_token")
        except HTTPError as e:
            logger.error(e)
            return None

        self.session.headers = {
            "Authorization": "Bearer " + token,
            "Ocp-Apim-Subscription-Key": self.primary_key
        }

        return token
