import asyncio
from typing import Any

import httpx

from ecommerce.logger import get_logger

logger = get_logger(__name__)


async def fetch_page(url: str, client: httpx.AsyncClient) -> str:
    r = await client.get(url)
    logger.info(f"[{r.status_code}]:{r.url}")
    r.raise_for_status()
    return r.text


async def has_key_value(o__: dict | list, k__: str, v__: Any = None, /) -> bool:
    """
    Returns `True` if the given key-value pair exists in the given object, `False` otherwise.

    Args:
        obj: The object to search.
        key: The key to search for.
        value: The value to search for.

    Returns:
        `True` if the key-value pair is found, `False` otherwise.
    """

    if not isinstance(o__, (dict, list)):
        return False
    if k__ in o__:
        if isinstance(o__, list):
            return True
        if v__ is None or o__[k__] == v__:
            return True

    iterator = o__.values() if isinstance(o__, dict) else o__
    tasks = [asyncio.create_task(has_key_value(i, k__, v__)) for i in iterator]
    return any(await asyncio.gather(*tasks))
