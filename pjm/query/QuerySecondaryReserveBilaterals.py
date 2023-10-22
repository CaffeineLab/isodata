"""QuerySecondaryReserveBilaterals - This message is used to query for the secondary reserve bilateral schedules that are operative
for a particular day. The query response returns all secondary reserve bilaterals for the
participant who is a party to the bilateral (as a buyer or a seller). This is a private report.
"""
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
