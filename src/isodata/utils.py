import re
from loguru import logger


def get_filename_from_headers(headers: dict) -> str:
    """Determine the header value for content-disposition and then
    return the matching filename if it exists.  We've seen the header
    key in multiple case formats, so solve for that."""

    try:
        key = [k for k in headers if k.lower() == 'content-disposition'][0]
        d = headers[key]
        return re.findall(r"filename=(.+)", d)[0]
    except TypeError as e:
        # probably None
        logger.info(f"No headers: {e}")
    except KeyError as e:
        # probably not a dict
        logger.info(f"Key Error: {e}")
    except IndexError as e:
        logger.info("No Filename in content-disposition")

    return None
