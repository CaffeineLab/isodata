"""QueryASBilaterals - This message is used to query for the latest known active subzone and reserve type to be
cleared per hour for the given operating day. This is a public report."""
import isodata.pjm.constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    query_filter = '<ProductType></ProductType>'
    if 'product_type' in kwargs:
        query_filter = '<ProductType>%s</ProductType>' % kwargs['product_type']

    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
            '<%s day="%s"/>' % (kwargs['report'], kwargs['market_day'].strftime('%Y-%m-%d')),
            query_filter,
            '</%s>' % kwargs['report'],
            '</QueryRequest>',
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
