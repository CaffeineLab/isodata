"""QueryInterfaceLimits - This query is for the report describing the hourly operating limits used in the day-ahead
scheduling process between PJM interfaces and neighboring control areas. This is a public
report.
This report is available daily when the Day Ahead Market result is approved on the day before the
operating day."""
# pylint:disable=duplicate-code
from ...pjm import constants as C
from ...pjm.helper import gen_xml


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
