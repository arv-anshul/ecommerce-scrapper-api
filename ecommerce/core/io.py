import functools
import os.path
from typing import Optional

import curler

from ecommerce.logger import get_logger

logger = get_logger(__name__)


@functools.lru_cache(8)
def get_requests_kwargs(fp: str, return_params: bool = False) -> Optional[dict]:
    logger.info(f"Reading: {fp!r}")
    requests_kws = (
        dict(curler.parse_file(fp).for_requests) if os.path.exists(fp) else None
    )
    # Remove url and method keys because they are passed explicitly
    if requests_kws:
        del requests_kws["url"]
        del requests_kws["method"]
        if not return_params:
            del requests_kws["params"]
        return requests_kws
