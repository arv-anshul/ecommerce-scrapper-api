import functools
from pathlib import Path

import curler

from ecommerce.logger import get_logger

logger = get_logger(__name__)


@functools.lru_cache(8)
def get_curl_command(fp: str) -> dict:
    logger.info(f"Reading: {fp!r}")
    if Path(fp).exists():
        requests_kws = dict(curler.parse_file(fp).for_requests)
        # Remove url and method keys because they are passed explicitly
        del requests_kws["url"]
        del requests_kws["method"]
        requests_kws.update({"params": {}})
        return requests_kws

    error_msg = f"Path: {fp!r}"
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)
