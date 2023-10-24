"""QueryBidNodes - Query for a list of all pricing nodes that have ever been referenced
by previous bids by the participant. This is a private report.

Note: No really good reason to use lxml other than to just show how it can be done.
"""
# pylint:disable=duplicate-code
from lxml import etree as ET
from ...pjm import constants as C


def make_request(report, pretty_print=False):
    """Generate the SOAP Document to send to the market."""

    env = ET.Element(ET.QName(C.SOAP_ENVELOPE, 'Envelope'), nsmap=C.SOAP_ENVELOPE_NS_MAP)
    env.set(ET.QName(C.SOAP_ENVELOPE, "encodingStyle"), C.SOAP_ENCCODING)
    ET.SubElement(env, ET.QName(C.SOAP_ENVELOPE, 'Header'), nsmap=C.SOAP_ENVELOPE_NS_MAP)
    body = ET.SubElement(env, ET.QName(C.SOAP_ENVELOPE, 'Body'), nsmap=C.SOAP_ENVELOPE_NS_MAP)
    req = ET.SubElement(body, ET.QName(C.PJM_EMKT_XMLNS, 'QueryRequest'), nsmap={None: C.PJM_EMKT_XMLNS})
    ET.SubElement(req, report)
    return ET.tostring(env, pretty_print=pretty_print, xml_declaration=True, encoding='UTF-8').decode('utf-8')


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""
    xml = make_request(kwargs['report'])

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  str(len(xml))
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
