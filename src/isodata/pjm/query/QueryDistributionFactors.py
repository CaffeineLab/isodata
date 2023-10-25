"""QueryDistributionFactors - You may query for a particular effective day and Aggregate nodes using the message described
below.
To query the system for a submitted distribution factors of a one or more aggregate nodes for a
given day.

You may query for a particular effective day and Aggregate nodes using the message described
below.  To query the system for a submitted distribution factors of a one or more aggregate nodes for a
given day.


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
