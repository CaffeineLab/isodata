"""QuerySolarForecast -  This message is used to query the solar forecast for an identified location for a hours of a given
day."""
import isodata.pjm.constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    disclaimer = """<DisclaimerAcceptance>
I accept the following terms of use regarding the Solar Forecast data:
THE RESALE, PUBLICATION, REPUBLICATION OR DISCLOSURE OF THIS DATA IS
STRICTLY PROHIBITED.
DATA AND ANALYSIS WAS PROVIDED BY UL SERVICES GROUP LLC ("UL") TO PJM
INTERCONNECTION, L.L.C. ("PJM").
PJM AND UL SHALL NOT HAVE ANY OBLIGATION OR LIABILITY TO ANY THIRD PARTY
REGARDING THIS INFORMATION.
 </DisclaimerAcceptance>"""

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
            disclaimer,
            '</%s>' % kwargs['report'],
            '</QueryRequest>'
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
