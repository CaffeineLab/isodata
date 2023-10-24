"""QueryMessages - This query returns messages that have been issued by the market operator. All messages are
considered public.


Optional query parameter specifying
the active date time to use when
querying messages. By default, the
current date and time are used.

Optional query parameter specifying
the priority threshold to use on filtering
the messages. All messages with a
priority of this threshold value or less
are returned. By default, the threshold
value is 999, meaning that all
messages are returned.

"""
# pylint:disable=duplicate-code
from datetime import datetime
from dateutil import parser
from ...pjm import constants as C


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""

    if 'active_date_time' in kwargs:
        active_filter = parser.parse(kwargs['active_date_time'])
    else:
        active_filter = datetime.utcnow()

    active_filter = active_filter.replace(microsecond=0).isoformat()
    active_filter = '<ActiveDateTime>%s</ActiveDateTime>' % active_filter

    priority_filter = '<PriorityThreshold>%s</PriorityThreshold>' % (
        kwargs['priority_threshold'] if 'priority_threshold' in kwargs else '999'
    )

    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
            '<%s>' % kwargs['report'],
            active_filter,
            priority_filter,
            '</%s>' % kwargs['report'],
            '</QueryRequest>',
            '</SOAP-ENV:Body>',
            '</SOAP-ENV:Envelope>',
        ])
    except KeyError as err:
        raise TypeError('[%s] Missing required field: %s for query.' % (kwargs['report'], err)) from err

    return {
        'xml': xml,
        'headers': {
            **C.PJM_BASE_HEADERS,
            'Cookie': 'pjmauth=' + token,
            'Content-length':  str(len(xml))
        },
        'url': C.PJM_EMKT_URL_QUERY
    }
