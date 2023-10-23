"""PJM Connector and Connection Utilities for ... connecting to PJM :) """
import json
from datetime import date, datetime
from importlib import import_module
import requests
from dateutil import parser
from requests.exceptions import SSLError, HTTPError, ReadTimeout
from loguru import logger
from isodata.connector import Connector
# pylint: disable=no-member


class PJMConnector(Connector):
    required = ['username', 'password', 'certificate']

    def query(self, **kwargs):

        # TODO: Clean up market_day validation.  For now - it's working.
        if 'market_day' in kwargs:
            if isinstance(kwargs['market_day'], str):
                try:
                    kwargs['market_day'] = parser.parse(kwargs['market_day'])
                except parser.ParserError as err:
                    logger.error("[%s:markety_day] %s" % (kwargs['report'], err))
                    return None
                except TypeError as err:
                    logger.error("[%s:markety_day] %s" % (kwargs['report'], err))
                    return None
            elif isinstance(kwargs['market_day'], datetime):
                pass
            elif isinstance(kwargs['market_day'], date):
                pass
            else:
                logger.error("[%s:markety_day] What did you pass in as a market day?" % kwargs['report'])
                return None

        package = (import_module('isodata.pjm.query.%s' % kwargs['report']).prepare(token=self.token, **kwargs))

        if package is None:
            return None

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
