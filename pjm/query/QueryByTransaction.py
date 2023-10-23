"""QueryByTransaction - The response to a successful query by transaction is a message that contains exactly what was
submitted by the transaction. This includes the entire message, including the SOAP envelope,
body elements, and <SubmitRequest> content."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml
from loguru import logger

def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryByTransaction xmlns="%s">' % C.PJM_EMKT_XMLNS,
            '<TransactionID>',
            kwargs['transaction_id'],
            '</TransactionID>',
            '</QueryByTransaction>',
            '</SOAP-ENV:Body>',
            '</SOAP-ENV:Envelope>',
        ])
    except KeyError as err:
        logger.error('[%s] Missing required field: transaction_id for query.' % err)
        return None

    return {
        'xml': xml,
        'headers': {
            'Host': 'marketsgateway.pjm.com',
            'SOAPAction': '/marketsgateway/xml/query',
            'Content-type': 'text/xml',
            'charset': 'UTF-8',
            'Accept': 'text/xml',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Cookie': 'pjmauth=' + token,
            'Content-length':  str(len(xml))
        },
        'url': C.PJM_EMKT_URL_QUERY,
    }
