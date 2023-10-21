"""Query for a list of all pricing nodes defined in the market"""
import isodata.pjm.constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    xml = "".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
        '<SOAP-ENV:Body>',
        '<QueryRequest xmlns="%s"><QueryNodeList day="%s"/></QueryRequest>' % (C.PJM_EMKT_XMLNS, kwargs['market_day']),
        '</SOAP-ENV:Body>',
        '</SOAP-ENV:Envelope>',
    ])

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
        'method': "post"
    }
