from isodata.pjm.connector import PJMConnector




def Session(market):
    if market.lower() == 'pjm':
        return PJMConnector()