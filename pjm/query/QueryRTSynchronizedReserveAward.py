"""QueryRTSynchronizedReserveAward - This message is used to query for the RT Synchronized Reserve Award for requested locations.
This is a private report."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""
    # TODO: Fix
    """<?xml version='1.0' encoding='UTF-8'?><Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><faultcode>Client</faultcode><faultstring>cvc-complex-type.2.4.b: The content of element 'QueryRTSynchronizedReserveAward' is not complete. One of '{"http://emkt.pjm.com/emkt/xml":All, "http://emkt.pjm.com/emkt/xml":LocationName, "http://emkt.pjm.com/emkt/xml":PortfolioName}' is expected.</faultstring></Body></Envelope>"""
    return None

    xml, content_length = gen_xml(with_filters=True, **kwargs)

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  content_length
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
