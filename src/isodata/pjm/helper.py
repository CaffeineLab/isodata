from loguru import logger
from ..pjm import constants as C


def gen_xml(with_filters=False, **kwargs):
    query_filter = ""
    if with_filters:

        if 'ProductType' in kwargs:
            query_filter = '<ProductType>%s</ProductType>' % kwargs['product_type']

        elif 'transaction_id' in kwargs:
            query_filter = '<TransactionID>%s</TransactionID>' % kwargs['transaction_id']

        elif with_filters == "<All/>":
            # default is 'all'

            if 'location_name' in kwargs:
                query_filter = '<LocationName>%s</LocationName>' % kwargs['location_name']
            elif 'portfolio_name' in kwargs:
                query_filter = '<PortfolioName>%s</PortfolioName>' % kwargs['portfolio_name']
            elif 'area_name' in kwargs:
                query_filter = '<AreaName>%s</AreaName>' % kwargs['area_name']
            else:
                query_filter = '<All/>'

        if 'hour' in kwargs:
            query_filter += '<Hour>%s</Hour>' % kwargs['hour']


    if 'disable_date' in kwargs:
        request = '<%s>' % kwargs['report']
    else:
        request = '<%s day="%s">' % (kwargs['report'], kwargs['market_day'].strftime('%Y-%m-%d'))



    try:
        xml = "".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
            '<SOAP-ENV:Body>',
            '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
            request,
            query_filter,
            '</%s>' % kwargs['report'],
            '</QueryRequest>',
            '</SOAP-ENV:Body>',
            '</SOAP-ENV:Envelope>',
        ])
    except KeyError as err:
        logger.error('[%s] Missing required field: %s for query.' % (kwargs['report'], err))
        return None

    return xml, str(len(xml))
