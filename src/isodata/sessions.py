"""Simple, simple factory for returning the right market connector."""
import sys
from loguru import logger
from .ercot.connector import ERCOTPublicConnector
from .pjm.connector import PJMConnector


def Session(market, loglevel=None):
    """Return requested market connector."""
    logger.remove()

    if loglevel is not None:
        logger.add(sys.stderr, level=loglevel)

    if market.lower() == 'pjm':
        return PJMConnector()
    if market.lower() == 'ercot_public':
        return ERCOTPublicConnector()
    return None
