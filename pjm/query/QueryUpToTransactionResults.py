"""QueryUpToTransactionResults - This message is used to query for up to transactions results. This is a private report."""
import isodata.pjm.constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    # TODO: implement optional TransactionID="999999.9"

    xml = "".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
        '<SOAP-ENV:Body>',
        '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
        '<QueryUpToTransactionResults day="%s"/>' % kwargs['market_day'].strftime("%Y-%m-%d"),
        '</QueryRequest>',
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
