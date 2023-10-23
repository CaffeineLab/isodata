SOAP_ENVELOPE = 'http://schemas.xmlsoap.org/soap/envelope/'
SOAP_ENCCODING = "http://schemas.xmlsoap.org/soap/encoding/"

SOAP_ENVELOPE_NS_MAP = {'SOAP-ENV': SOAP_ENVELOPE}
PJM_EMKT_XMLNS = 'http://emkt.pjm.com/emkt/xml'
PJM_EMKT_URL_QUERY = "https://marketsgateway.pjm.com/marketsgateway/xml/query"
PJM_EMKT_URL_TRANSACTION = "https://marketsgateway.pjm.com/marketsgateway/xml/querybytransaction"

PJM_BASE_HEADERS = {
    'Host': 'marketsgateway.pjm.com',
    'SOAPAction': '/marketsgateway/xml/query',
    'Content-type': 'text/xml',
    'charset': 'UTF-8',
    'Accept': 'text/xml',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Cookie': '',
    'Content-length':  '0'
}