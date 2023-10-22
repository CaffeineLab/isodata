"""QueryByTransaction - The response to a successful query by transaction is a message that contains exactly what was
submitted by the transaction. This includes the entire message, including the SOAP envelope,
body elements, and <SubmitRequest> content."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    xml, content_length = gen_xml(with_filters=True, **kwargs)

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  content_length
        },
        'url': C.PJM_EMKT_URL_TRANSACTION,
        'method': "post"
    }
