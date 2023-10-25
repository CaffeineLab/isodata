"""QueryDSRScheduleOfferUpdate - To query the system for schedule detail update
<QueryRequest>
 <QueryDSRScheduleOfferUpdate location="string" schedule="string"
day="yyyy-mm-dd"/>
"""
# pylint:disable=duplicate-code
from ...pjm import constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""
    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
            '<%s location="%s" schedule="%s" day="%s"/>' % (
                kwargs['report'],
                kwargs['location'],
                kwargs['schedule'],
                kwargs['market_day'].strftime('%Y-%m-%d')),

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
