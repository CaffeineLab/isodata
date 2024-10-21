import requests
from requests.exceptions import HTTPError, ReadTimeout, SSLError
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed
from ..connector import Connector
from ..utils import get_filename_from_headers


class ERCOTPrivateConnector(Connector):
    required = ['cert']

    def __init__(self):
        self.cert = None

    def fetch_doc(self, document, save_path):
        """Convert the document id into the URL for fetching the resource."""
        url = f"https://mis.ercot.com/misdownload/servlets/mirDownload?doclookupId={document[0]}"
        return self.fetch_url(url, save_path)

    def fetch_url(self, url, save_path):
        """Fetch the document resource (.zip/.csv/.???) and save it to the folder."""

        if self.token is None:
            logger.warning("Connector not authenticated to retrieve resource.")
            return None

        logger.info(f"Fetching: {url}")

        response = None
        try:
            response = requests.get(
                url,
                cert=self.cert,
                timeout=10)
            response.raise_for_status()
        except HTTPError as err:
            logger.error(err)
            if response.status_code == 403:
                logger.error('No permission for this resource.')
            return None
        except ReadTimeout as err:
            logger.error(err)
            return None

        # Save the file with the same filename as the source to the dest folder.
        fname = get_filename_from_headers(response.headers)

        if fname is None:
            return None

        out_file = save_path / fname

        with open(out_file, 'wb') as f:
            f.write(response.content)

        return out_file


    def fetch_listing(self, emil_id=None, report_type_id=None, page=None):
        """Fetch download list for requested report."""


        if report_type_id is not None:
            url = f"https://mis.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId={report_type_id}"
        else:
            url = f"https://mis.ercot.com/secure/data-products/markets/day-ahead-market?id={emil_id}"

        if self.token is None:
            logger.warning('No token - Cannot fetch url')
            return None

        # url = f"https://mis.ercot.com/secure/data-products/markets/day-ahead-market?id={emil_id}"

        if page is not None:
            assert page > 0, 'page must be greater than 0'
            url += f"?page={page}"

        results = []

        try:
            response = requests.get(
                url=url,
                timeout=10,
                cert=self.cert
            )
            response.raise_for_status()

        except HTTPError as err:

            if response.status_code == 400:
                logger.error('Requested non-existent page.')
                logger.error(err)

            elif response.status_code == 401:
                logger.error('Token expired?')
                logger.error(err)
                self.token = None
            else:
                logger.error(err)
                logger.error(response.text)

            return results, 0

        except SSLError as err:
            logger.error(err)
            logger.info('If authed, you should not see this error')
            return None
        except HTTPError as err:
            logger.error(err)
            logger.error(response.text)
            return None
        except ReadTimeout as err:
            logger.error(err)
            return None


        if response.json().get('ListDocsByRptTypeRes') is None:
            return results, 0

        # Get the meta results from the call.  Record count, page count, etc.
        meta = response.json().get('_meta')



        for document in [x['Document'] for x in response.json()['ListDocsByRptTypeRes']['DocumentList']]:
            results.append([
                document['DocID'],
                document['PublishDate'],
                document['ConstructedName']
            ])

        return results, meta



    def get_token(self):

        # Verify that the cert and key file exist.
        if self.cert[0].exists() is False:
            logger.error("Supplied certificate path does not exist.")
            return None

        if self.cert[1].exists() is False:
            logger.error("Supplied key path does not exist.")
            return None


        return 'working-ish'


class ERCOTPublicConnector(Connector):

    required = ['username', 'password', 'primary_key', 'auth_url']

    def __init__(self):
        self.username = None
        self.password = None
        self.primary_key = None
        self.auth_url = None

    def headers(self):
        return {
            "Authorization": "Bearer " + self.token,
            "Ocp-Apim-Subscription-Key": self.primary_key
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_url(self, url, save_path):
        """Fetch the document and save it to the path."""

        if self.token is None:
            self.token = self.get_token()

        logger.info("Fetching URL from ERCOT")

        try:
            response = requests.get(url, headers=self.headers(), timeout=10)
            response.raise_for_status()
        except HTTPError as err:
            logger.error(err)
            logger.error(response.text)
            if response.status_code == 401:
                logger.error('Token expired?')
                self.token = None
            return None
        except ReadTimeout as err:
            logger.error(err)
            return None

        fname = get_filename_from_headers(response.headers)
        if fname is None:
            return None

        out_file = save_path / fname
        with open(out_file, 'wb') as f:
            f.write(response.content)

        return out_file

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

        if self.token is None:
            self.token = self.get_token()

        results = []

        try:
            response = requests.get(url, headers=self.headers(), timeout=10)
            response.raise_for_status()

        except HTTPError as err:

            if response.status_code == 400:
                logger.error('Requested non-existent page.')
                logger.error(err)

            elif response.status_code == 401:
                logger.error('Token expired?')
                logger.error(err)
                self.token = None
            else:
                logger.error(err)
                logger.error(response.text)

            return results, 0
        except ReadTimeout as err:
            logger.error(err)
            return results, 0

        if response.json().get('archives') is None:
            return results, 0

        # Get the meta results from the call.  Record count, page count, etc.
        meta = response.json().get('_meta')

        for row in response.json().get('archives'):
            results.append([
                row['docId'],
                row['postDatetime'],
                row['_links']['endpoint']['href']
            ])

        return results, meta['totalRecords']

    def get_token(self):
        """Get the tokenId from the ERCOT Public API service"""

        logger.info("Generating and Submitting Token Request for %s." % self.username)
        url = self.auth_url.format(username=self.username, password=self.password)

        try:
            response = requests.post(url=url, timeout=30)
            response.raise_for_status()
            return response.json().get("access_token")
        except HTTPError as e:
            logger.error(e)

        return None
