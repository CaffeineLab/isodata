"""QueryPseudoTransactionResults - This message is used to query for pseudo tie transaction results. This is a private report.
The data is published for each operating day."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""
    # TODO: QueryPseudoTransactionResults not in C.PJM_QUERY_REPORT_LIST

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
