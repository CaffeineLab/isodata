"""QueryAllDSRScheduleSelection - To request all schedules associated with a load response location or the locations of a portfolio
<QueryRequest>
 <QueryAllDSRScheduleSelection day="yyyy-mm-dd" available="xxx" >
 <All/>
 <LocationName>xxx</LocationName>
 <PortfolioName>xxx</PortfolioName>
 </QueryAllDSRScheduleSelection>
</QueryRequest>
"""
from ...pjm import constants as C
from ...pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    if 'available' not in kwargs:
        raise TypeError("[%s] Missing required field: 'available' for query." % kwargs['report'])

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
