"""Simple, simple factory for returning the right market connector."""
from .ercot.connector import ERCOTPublicConnector
from .pjm.connector import PJMConnector


def Session(market):
    """Return requested market connector."""
    if market.lower() == 'pjm':
        return PJMConnector()
    if market.lower() == 'ercot_public':
        return ERCOTPublicConnector()
    return None
