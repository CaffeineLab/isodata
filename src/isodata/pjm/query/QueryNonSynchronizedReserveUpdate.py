"""QueryNonSynchronizedReserveUpdate - You may query for a particular market day and resource location using the message described
below.
To query for submitted update data use the following query request:
<QueryRequest>
 <QueryNonSynchronizedReserveUpdate day="yyyy-mm-dd">
 <All/>
 <LocationName>zzz</LocationName>
 <PortfolioName>zzz</PortfolioName>
 </QueryNonSynchronizedReserveUpdate>
</QueryRequest>

"""
# pylint:disable=duplicate-code
from ...pjm import constants as C
from ...pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    xml, content_length = gen_xml(with_filters="<All/>", disable_date=True, **kwargs)
    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  content_length
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
