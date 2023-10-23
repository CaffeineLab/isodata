"""QueryMarketPrices - This query returns the day-ahead market clearing prices for the requested locations. This is a
public report. The report is an hourly report for the requested operating day.
The market clearing prices are available daily when the Day Ahead Market result is approved on
the day before the operating day."""
# pylint:disable=duplicate-code
import isodata.pjm.constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    if 'location_name' in kwargs:
        query_filter = '<LocationName>%s</LocationName>' % kwargs['location_name']
    elif 'portfolio_name' in kwargs:
        query_filter = '<PortfolioName>%s</PortfolioName>' % kwargs['portfolio_name']
    elif 'area_name' in kwargs:
        query_filter = '<AreaName>%s</AreaName>' % kwargs['area_name']
    else:
        query_filter = '<All/>'


    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
            '<%s type="%s" day="%s">' % (kwargs['report'], kwargs['type'], kwargs['market_day'].strftime('%Y-%m-%d')),
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
