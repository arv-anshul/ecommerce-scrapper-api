import json

from bs4 import BeautifulSoup

from ecommerce import types
from ecommerce.parser._parser import logger


async def parse_flipkart_page_json(html: str) -> types.JSON:
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.select_one("#is_script")

    if script_tag is None:
        msg = "No script tag with id='#is_script' found in search page html content."
        logger.error(msg)
        raise ValueError(msg)
    # Clean text to parse JSON content
    text = script_tag.text.removeprefix("window.__INITIAL_STATE__ = ").removesuffix(";")
    content = json.loads(text)
    return content
