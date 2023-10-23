"""QueryRegulationResults - This message is used to query for the regulation market results showing the market clearing
prices and cleared regulation MW per hour of a given operating day. This is a public report.
This report is published and available hourly during the operating day."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    # TODO: Fix error.
    """<?xml version='1.0' encoding='UTF-8'?><Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><faultcode>Client</faultcode><faultstring>cvc-complex-type.2.1: Element 'QueryRegulationResults' must have no character or element information item [children], because the type's content type is empty.</faultstring></Body></Envelope>"""
    return None

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
