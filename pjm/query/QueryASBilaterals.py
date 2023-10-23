"""QueryASBilaterals - This message is used to query for the latest known active subzone and reserve type to be
cleared per hour for the given operating day. This is a public report."""
import isodata.pjm.constants as C
from isodata.pjm.helper import gen_xml
from loguru import logger


def prepare(token, **kwargs):
    """prepare and return all the components of the requests call."""


    # TODO:  may not be implemented????
    """
<?xml version='1.0' encoding='UTF-8'?><Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><faultcode>Client</faultcode><faultstring>cvc-complex-type.2.4.a: Invalid content was found starting with element '{"http://emkt.pjm.com/emkt/xml":QueryASBilaterals}'. 
One of '{"http://emkt.pjm.com/emkt/xml":QueryBindingLimits,
"http://emkt.pjm.com/emkt/xml":QueryBidNodes,
"http://emkt.pjm.com/emkt/xml":QueryDemandBid,
"http://emkt.pjm.com/emkt/xml":QueryDemandSummary,
"http://emkt.pjm.com/emkt/xml":QueryDispatchLambda,
"http://emkt.pjm.com/emkt/xml":QueryDistributionFactors,
"http://emkt.pjm.com/emkt/xml":QueryDSRDetail,
"http://emkt.pjm.com/emkt/xml":QueryDSRRegistration,
"http://emkt.pjm.com/emkt/xml":QueryDSRRegulationOffer,
"http://emkt.pjm.com/emkt/xml":QueryDSRRegulationUpdate,
"http://emkt.pjm.com/emkt/xml":QueryDSRSRREGAward,
"http://emkt.pjm.com/emkt/xml":QueryDSRSchedules,
"http://emkt.pjm.com/emkt/xml":QueryDSRScheduleDefinitions,
"http://emkt.pjm.com/emkt/xml":QueryDSRScheduleDetail,
"http://emkt.pjm.com/emkt/xml":QueryDSRScheduleOffer,
"http://emkt.pjm.com/emkt/xml":QueryDSRScheduleOfferUpdate,
"http://emkt.pjm.com/emkt/xml":QueryDSRScheduleCompositeOffer,
"http://emkt.pjm.com/emkt/xml":QueryDSRScheduleSelection,
"http://emkt.pjm.com/emkt/xml":QueryDSRUpdate,
"http://emkt.pjm.com/emkt/xml":QueryInterfaceLimits,
"http://emkt.pjm.com/emkt/xml":QueryMarketPrices,
"http://emkt.pjm.com/emkt/xml":QueryMarketResults,
"http://emkt.pjm.com/emkt/xml":QueryMessages,
"http://emkt.pjm.com/emkt/xml":QueryNetTieSchedule,
"http://emkt.pjm.com/emkt/xml":QueryNodeList,
"http://emkt.pjm.com/emkt/xml":QueryPortfolios,
"http://emkt.pjm.com/emkt/xml":QueryRASchedMW,
"http://emkt.pjm.com/emkt/xml":QueryRegulationBilaterals,
"http://emkt.pjm.com/emkt/xml":QueryRegulationOffer,
"http://emkt.pjm.com/emkt/xml":QueryRegulationResults,
"http://emkt.pjm.com/emkt/xml":QueryRegulationUpdate,
"http://emkt.pjm.com/emkt/xml":QuerySchedReserveBilaterals,
"http://emkt.pjm.com/emkt/xml":QueryScheduleDefinitions,
"http://emkt.pjm.com/emkt/xml":QueryScheduleDetail,
"http://emkt.pjm.com/emkt/xml":QueryScheduleDetailUpdate,
"http://emkt.pjm.com/emkt/xml":QueryScheduleOffer,
"http://emkt.pjm.com/emkt/xml":QueryScheduleUpdate,
"http://emkt.pjm.com/emkt/xml":QueryScheduleOfferPriceCaps,
"http://emkt.pjm.com/emkt/xml":QueryScheduleCompositeOffer,
"http://emkt.pjm.com/emkt/xml":QueryScheduleSelection,
"http://emkt.pjm.com/emkt/xml":QueryScheduleSwitch,
"http://emkt.pjm.com/emkt/xml":QueryAllDSRScheduleDetail,
"http://emkt.pjm.com/emkt/xml":QueryAllDSRScheduleSelection,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleDetail,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleDetailUpdate,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleOffer,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleUpdate,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleSelection,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleAvailabilityUpdate,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleGasNomination,
"http://emkt.pjm.com/emkt/xml":QueryAllScheduleRestriction,
"http://emkt.pjm.com/emkt/xml":QueryThresholds,
"http://emkt.pjm.com/emkt/xml":QueryUnitDetail,
"http://emkt.pjm.com/emkt/xml":QueryUnitParameterLimit,
"http://emkt.pjm.com/emkt/xml":QueryExceptionParameterLimits,
"http://emkt.pjm.com/emkt/xml":QueryGetUnitParameterLimits,
"http://emkt.pjm.com/emkt/xml":QueryUnitSchedules,
"http://emkt.pjm.com/emkt/xml":QueryUnitUpdate,
"http://emkt.pjm.com/emkt/xml":QueryUnitRampRates,
"http://emkt.pjm.com/emkt/xml":QueryVirtualBid,
"http://emkt.pjm.com/emkt/xml":QueryWeatherForecast,
"http://emkt.pjm.com/emkt/xml":QueryIFPUnitUpdate,
"http://emkt.pjm.com/emkt/xml":QueryIFPUnitOffer,
"http://emkt.pjm.com/emkt/xml":QueryIFPAreaForecast,
"http://emkt.pjm.com/emkt/xml":QueryOPCFuelTypes,
"http://emkt.pjm.com/emkt/xml":QueryOPCOpportunityCosts,
"http://emkt.pjm.com/emkt/xml":QueryOPCUnitParameters,
"http://emkt.pjm.com/emkt/xml":QueryOPCDeliveredFuel,
"http://emkt.pjm.com/emkt/xml":QueryOPCDeliveredFuelMonthly,
"http://emkt.pjm.com/emkt/xml":QueryOPCOutages,
"http://emkt.pjm.com/emkt/xml":QueryOPCForecastedAllowance,
"http://emkt.pjm.com/emkt/xml":QueryUpToTransactions,
"http://emkt.pjm.com/emkt/xml":QueryNewUpToTransactionID,
"http://emkt.pjm.com/emkt/xml":QueryUpToTransactionResults,
"http://emkt.pjm.com/emkt/xml":QueryPseudoTieTransactions,
"http://emkt.pjm.com/emkt/xml":QueryPseudoTieTransactionResults,
"http://emkt.pjm.com/emkt/xml":QueryPRDResponseCurve,
"http://emkt.pjm.com/emkt/xml":QueryPRDHourly,
"http://emkt.pjm.com/emkt/xml":QueryWindForecast,
"http://emkt.pjm.com/emkt/xml":QueryDASchedMW,
"http://emkt.pjm.com/emkt/xml":QueryDemandBidCap,
"http://emkt.pjm.com/emkt/xml":QueryScheduleAvailabilityUpdate,
"http://emkt.pjm.com/emkt/xml":QueryScheduleGasNomination,
"http://emkt.pjm.com/emkt/xml":QueryScheduleRestriction,
"http://emkt.pjm.com/emkt/xml":QueryRTScheduleUseCost,
"http://emkt.pjm.com/emkt/xml":QueryFuelTypes,
"http://emkt.pjm.com/emkt/xml":QueryTPSScheduleSwitch,
"http://emkt.pjm.com/emkt/xml":QuerySolarForecast,
"http://emkt.pjm.com/emkt/xml":QueryUnitLimitations,
"http://emkt.pjm.com/emkt/xml":QueryFuelPriceExceptions,
"http://emkt.pjm.com/emkt/xml":QueryStorageUpdate,
"http://emkt.pjm.com/emkt/xml":QueryDASynchronizedReserveResults,
"http://emkt.pjm.com/emkt/xml":QueryRTSynchronizedReserveResults,
"http://emkt.pjm.com/emkt/xml":QueryDAPrimaryReserveResults,
"http://emkt.pjm.com/emkt/xml":QueryRTPrimaryReserveResults,
"http://emkt.pjm.com/emkt/xml":QueryDA30MinuteReserveResults,
"http://emkt.pjm.com/emkt/xml":QueryRT30MinuteReserveResults,
"http://emkt.pjm.com/emkt/xml":QueryNonSynchronizedReserveOffer,
"http://emkt.pjm.com/emkt/xml":QueryNonSynchronizedReserveUpdate,
"http://emkt.pjm.com/emkt/xml":QuerySecondaryReserveOffer,
"http://emkt.pjm.com/emkt/xml":QuerySecondaryReserveUpdate,
"http://emkt.pjm.com/emkt/xml":QuerySynchronizedReserveOffer,
"http://emkt.pjm.com/emkt/xml":QuerySynchronizedReserveUpdate,
"http://emkt.pjm.com/emkt/xml":QueryDSRSecondaryReserveOffer,
"http://emkt.pjm.com/emkt/xml":QueryDSRSecondaryReserveUpdate,
"http://emkt.pjm.com/emkt/xml":QueryDSRSynchronizedReserveOffer,
"http://emkt.pjm.com/emkt/xml":QueryDSRSynchronizedReserveUpdate,
"http://emkt.pjm.com/emkt/xml":QueryRegulationAward,
"http://emkt.pjm.com/emkt/xml":QueryDASynchronizedReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryRTSynchronizedReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryDANonSynchronizedReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryDASecondaryReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryRTSecondaryReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryDSRRegulationAward,
"http://emkt.pjm.com/emkt/xml":QueryDSRDASynchronizedReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryDSRRTSynchronizedReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryDSRDASecondaryReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryDSRRTSecondaryReserveAward,
"http://emkt.pjm.com/emkt/xml":QueryActiveSubzone,
"http://emkt.pjm.com/emkt/xml":QuerySecondaryReserveBilaterals,
"http://emkt.pjm.com/emkt/xml":QuerySynchronizedReserveBilaterals,
"http://emkt.pjm.com/emkt/xml":QueryNonSynchronizedReserveBilaterals
}' is expected.</faultstring></Body></Envelope>


"""

    return None

    query_filter = '<ProductType></ProductType>'
    if 'product_type' in kwargs:
        query_filter = '<ProductType>%s</ProductType>' % kwargs['product_type']


    xml = "".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="%s" xmlns:SOAP-ENV="%s">' % (C.SOAP_ENCCODING, C.SOAP_ENVELOPE),
        '<SOAP-ENV:Body>',
        '<QueryRequest xmlns="%s">' % C.PJM_EMKT_XMLNS,
        '<QueryASBilaterals day="%s"/>' % kwargs['market_day'].strftime('%Y-%m-%d'),
        query_filter,
        '</QueryASBilaterals>',
        '</QueryRequest>',
        '</SOAP-ENV:Body>',
        '</SOAP-ENV:Envelope>',
    ])

    return {
        'xml': xml,
        'headers': {
            'Host': 'marketsgateway.pjm.com',
            'SOAPAction': '/marketsgateway/xml/query',
            'Content-type': 'text/xml',
            'charset': 'UTF-8',
            'Accept': 'text/xml',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Cookie': 'pjmauth=' + token,
            'Content-length':  str(len(xml))
        },
        'url': C.PJM_EMKT_URL_QUERY,
    }

