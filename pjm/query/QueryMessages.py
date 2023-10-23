"""QueryMessages - This query returns messages that have been issued by the market operator. All messages are
considered public.

<QueryRequest>
 <QueryMessages>
 <ActiveDateTime>yyyy-mm-ddThh:mm:ss</ActiveDateTime>
 <PriorityThreshold>xxx</PriorityThreshold>
 </QueryMessages>
</QueryRequest>

"""
# TODO: Implement QueryMessages.

import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""
    return None

    xml, content_length = gen_xml(with_filters="<All/>", **kwargs)

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length': content_length
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
