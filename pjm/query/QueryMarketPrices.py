"""QueryMarketPrices - This query returns the day-ahead market clearing prices for the requested locations. This is a
public report. The report is an hourly report for the requested operating day.
The market clearing prices are available daily when the Day Ahead Market result is approved on
the day before the operating day."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    xml, content_length = gen_xml(with_filters="<All/>", **kwargs)

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  content_length
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
