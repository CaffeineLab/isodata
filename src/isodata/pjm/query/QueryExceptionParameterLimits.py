"""QueryExceptionParameterLimits - You may query for a particular effective day and weather point using the message described
below.
To query the system for submitted exceptions for a given interval

"""
# pylint:disable=duplicate-code
from ...pjm import constants as C
from dateutil.parser import parse


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    if 'location_name' in kwargs:
        query_filter = '<LocationName>%s</LocationName>' % kwargs['location_name']
    elif 'portfolio_name' in kwargs:
        query_filter = '<PortfolioName>%s</PortfolioName>' % kwargs['portfolio_name']
    else:
        query_filter = '<All/>'


    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
            '<%s day="%s">' % (kwargs['report'], kwargs['market_day'].strftime('%Y-%m-%d')),
            query_filter,
            '<StartDate>%s</StartDate>' % parse(kwargs['start_date']).strftime('%Y-%m-%d'),
            '<EndDate>%s</EndDate>' % parse(kwargs['end_date']).strftime('%Y-%m-%d'),
            '<Status>%s</Status>' % kwargs['status'],
            '<RequestType>%s</RequestType>' % kwargs['request_type'],
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
