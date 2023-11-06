from typing import Any

import httpx

from ecommerce.logger import get_logger

logger = get_logger(__name__)


async def fetch_page(url: str, client: httpx.AsyncClient) -> str:
    r = await client.get(url)
    logger.info(f"[{r.status_code}]:{r.url}")
    r.raise_for_status()
    return r.text


def has_key_value(obj: dict | list, key: str, value: Any = None) -> bool:
    if isinstance(obj, dict):
        if key in obj and (obj[key] == value or value is None):
            return True
        else:
            for v in obj.values():
                if has_key_value(v, key, value):
                    return True
    elif isinstance(obj, list):
        for i in obj:
            if has_key_value(i, key, value):
                return True
    return False
