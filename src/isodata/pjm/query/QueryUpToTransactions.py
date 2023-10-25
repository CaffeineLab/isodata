"""QueryUpToTransactions - You may query for a particular Up To Transaction using either a transaction id and market day or
for a source/sink location(s) and day using the message described below.
To query for a submitted Up To Transaction data using a Transaction ID use the following query
request:


<QueryRequest>
 <QueryUpToTransactions day="yyyy-mm-dd">
 <TransactionID>999999.9</TransactionID>
 </QueryUpToTransactions>
</QueryRequest>
"""
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
