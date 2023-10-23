"""QueryDemandSummary - This message format is used to query for the day-ahead demand summary reporting the overall
system demand forecast versus cleared energy by area. The day-ahead summary also includes
the reserve requirement for each area.
Data is available when the day-ahead market closes on the day-ahead of the operating day"""
# pylint:disable=duplicate-code
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    xml, content_length = gen_xml(with_filters=False, **kwargs)

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  content_length
        },
        'url': C.PJM_EMKT_URL_QUERY
    }


