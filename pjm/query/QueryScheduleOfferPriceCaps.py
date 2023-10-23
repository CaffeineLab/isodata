"""QueryScheduleOfferPriceCaps - This query returns the price caps for schedule offer update curve if any price point of the curve
goes over the $1000 threshold limit for the requested day and location or portfolio. If there is no
price point of the curve that goes above the limit, there will be no data given for that period/hour.
This is a private report. """
# pylint:disable=duplicate-code
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