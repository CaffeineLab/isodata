"""QueryScheduleOffer - Two different schedule query requests are provided. You may query for a schedule offer by
specifying a particular schedule and generator unit name. The result if a single schedule offer
that matches the request parameters. Or, you can request all schedules associated with a given
unit or the units in a specified portfolio. The all qualifier can specify all schedules or all of the
schedules that are available for a particular market date (day ahead or balancing).
To query the market for a specific submitted schedule offers, issue the following QueryRequest
message:


<QueryRequest>
 <QueryScheduleOffer location="xxx" schedule="xx" day="yyyy-mm-dd"/>
</QueryRequest>



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
