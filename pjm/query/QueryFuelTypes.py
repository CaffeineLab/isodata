"""QueryFuelTypes - This query will return a list of all valid fuel types. This is a public report.
The Fuel Type list is updated as needed by PJM."""
import isodata.pjm.constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    xml = "".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
        '<SOAP-ENV:Body>',
        '<QueryRequest xmlns="%s"><QueryFuelTypes/></QueryRequest>' % C.PJM_EMKT_XMLNS,
        '</SOAP-ENV:Body>',
        '</SOAP-ENV:Envelope>',
    ])

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  str(len(xml))
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
