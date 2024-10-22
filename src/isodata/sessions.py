"""Simple, simple factory for returning the right market connector."""
import sys
from loguru import logger
from .ercot.connector import ERCOTPublicConnector
from .ercot.connector import ERCOTPrivateConnector
from .pjm.connector import PJMConnector


def Session(market, loglevel=None):
    """Return requested market connector."""
    logger.remove()

    if loglevel is not None:
        log_fmt = ("<green>{time:mm:ss}</green> | <level>{level: <8}</level> | "
                   "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        logger.add(sys.stderr, level=loglevel, format=log_fmt)

    if market.lower() == 'pjm':
        return PJMConnector()
    if market.lower() == 'ercot_public':
        return ERCOTPublicConnector()
    if market.lower() == 'ercot_private':
        return ERCOTPrivateConnector()
    return None
