"""QuerySolarForecast -  This message is used to query the solar forecast for an identified location for a hours of a given
day.

<QueryRequest>
 <QuerySolarForecast day="yyyy-mm-dd">
 <All/>
 <LocationName>xxx</LocationName>
 <PortfolioName>xxx</PortfolioName>
 <DisclaimerAcceptance>
I accept the following terms of use regarding the Solar Forecast data:
THE RESALE, PUBLICATION, REPUBLICATION OR DISCLOSURE OF THIS DATA IS
STRICTLY PROHIBITED.
DATA AND ANALYSIS WAS PROVIDED BY UL SERVICES GROUP LLC ("UL") TO PJM
INTERCONNECTION, L.L.C. ("PJM").
PJM AND UL SHALL NOT HAVE ANY OBLIGATION OR LIABILITY TO ANY THIRD PARTY
REGARDING THIS INFORMATION.
 </DisclaimerAcceptance>
 </QuerySolarForecast>
</QueryRequest>
# TODO: Implement QuerySolarForecast
"""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml


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
