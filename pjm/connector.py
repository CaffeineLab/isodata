"""PJM Connector and Connection Utilities for ... connecting to PJM :) """
import json
from importlib import import_module
import requests
from requests.exceptions import SSLError, HTTPError, ReadTimeout
from loguru import logger
from isodata.connector import Connector
# pylint: disable=no-member


class PJMConnector(Connector):
    required = ['username', 'password', 'certificate']

    def fetch(self, **kwargs):
        package = (import_module('isodata.pjm.public.%s' % kwargs['method']).prepare(token=self.token, **kwargs))
        response = None
        try:
            response = requests.post(url=package['url'], headers=package['headers'], data=package['xml'], timeout=10)
            response.raise_for_status()
            return response.text
        except HTTPError as err:
            logger.error(err)
            if response.status_code == 405:
                logger.error('Check the url to see if it is changed or we are not posting to correct endpoint')
            elif response.status_code == 401:
                logger.error('Check the username to see if it is correct.  Has it been force changed?')
        except KeyError as err:
            logger.error("An enexpected error where PJM returns an empty document.")
            logger.error(err)
            logger.error(response.text)
        except ReadTimeout as err:
            logger.error(err)
            if len(package['xml']) < 100:
                logger.warning("Check content of XML in package.  Seems light.")
        return None



    def get_token(self):
        """Get the tokenId from the PJM Authentication service"""

        logger.info("Generating and Submitting Token Request for %s." % self.username)
        headers = {'Content-Type': 'application/json',
                   'X-OpenAM-Username': self.username,
                   'X-OpenAM-Password': self.password,
                   'Accept': 'text/xml',
                   'charset': 'UTF-8',
                   'Cache-Control': 'no-cache',
                   'Pragma': 'no-cache'
                   }

        try:
            response = requests.post(url="https://sso.pjm.com/access/authenticate/pjmauthcert",
                                     headers=headers,
                                     cert=(self.certificate[0], self.certificate[1]),
                                     timeout=30)
            response.raise_for_status()
        except HTTPError as e:
            logger.error(e)
            return None
        except SSLError as e:
            logger.error(e)
            logger.info('Good chance the certificate or key are invalid.')
            return None

        json_results = json.loads(response.text)
        return json_results['tokenId']
