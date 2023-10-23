"""QueryByTransaction - The response to a successful query by transaction is a message that contains exactly what was
submitted by the transaction. This includes the entire message, including the SOAP envelope,
body elements, and <SubmitRequest> content."""
import isodata.pjm.constants as C


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
        raise TypeError('[%s] Missing required field: %s for query.' % (kwargs['report'], err)) from err

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  str(len(xml))
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
