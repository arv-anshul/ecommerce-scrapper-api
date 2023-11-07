import json
from typing import Any

import httpx
from bs4 import BeautifulSoup

from ecommerce import types
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


async def get_PageData(html: str) -> types.JSON:
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.select_one("#is_script")

    if script_tag is None:
        msg = "No script tag with id='#is_script' found in search page html content."
        logger.error(msg)
        raise ValueError(msg)
    text = script_tag.text[27:-1]  # Clean text to parse JSON content
    content = json.loads(text)
    return content
