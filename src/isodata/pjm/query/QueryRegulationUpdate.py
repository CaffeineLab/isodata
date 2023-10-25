"""QueryRegulationUpdate - You may query for a particular effective day and generator unit location using the message
described below.
To query the market for a submitted Regulation Update data and receive all the hourly intervals
submitted:

<QueryRequest>
 <QueryRegulationUpdate day="yyyy-mm-dd">
 <All/>
 <LocationName>zzz</LocationName>
 <PortfolioName>zzz</PortfolioName>
 </QueryRegulationUpdate>
</QueryRequest>


"""
# pylint:disable=duplicate-code
from ...pjm import constants as C
from ...pjm.helper import gen_xml


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
