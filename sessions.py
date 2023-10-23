"""Simple simple factory for returning the right market connector."""
from isodata.pjm.connector import PJMConnector


def Session(market):
    """Return requested market connector."""
    if market.lower() == 'pjm':
        return PJMConnector()
    return None
