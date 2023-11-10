import asyncio
import json
import urllib.parse
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from ecommerce import types
from ecommerce.core import io
from ecommerce.core.errors import SearchPageError
from ecommerce.logger import get_logger
from ecommerce.parser import Pagination, fetch_page, has_key_value
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.parser.search_page import BaseSearchPageHTMLParser
from ecommerce.validator.flipkart import FlipkartSearchPageProductSummaryModel

logger = get_logger(__name__)
SEARCH_PAGE_CURL_PATH = "configs/curl/flipkart.searchPage"


class FlipkartSearchPageError(SearchPageError):
    """Exception specific to Flipkart's SearchPage."""


class FlipkartSearchPage(BaseSearchPageHTMLParser):
    def __init__(
        self,
        search_query: str,
        pages: types.PagesLike = range(1, 6),
        params: Optional[types.URLParams] = None,
    ):
        self.search_query = search_query
        self.pages = Pagination(pages)
        self.__cached_html_pages = {}

        self.requests_kws = io.get_curl_command(SEARCH_PAGE_CURL_PATH)
        self.requests_kws.update({"params": params}) if params else ...

    @property
    def urls(self) -> set[str]:
        return {
            urllib.parse.quote(
                f"https://flipkart.com/search?page={page}&q={self.search_query}",
                safe="/?:=&",
            )
            for page in self.pages
        }

    @property
    def get_all_cached_html_pages(self) -> dict[str, str]:
        return self.__cached_html_pages

    async def get_html_pages(self) -> list[str]:
        responses = []
        async with httpx.AsyncClient(
            **self.requests_kws,
            follow_redirects=True,
            timeout=3,
        ) as client:
            for url in self.urls:
                cached_page = self.__cached_html_pages.get(url)
                if cached_page:
                    responses.append(cached_page)
                else:
                    response_txt = await fetch_page(url, client)
                    responses.append(response_txt)
                    self.__cached_html_pages[url] = response_txt
        return responses

    @staticmethod
    async def get_ItemList(html: str) -> types.JSON:
        soup = BeautifulSoup(html, "html.parser")
        script_tags = soup.select("#jsonLD")
        for tag in script_tags:
            json_content: types.JSON = json.loads(tag.text)
            if await has_key_value(
                json_content, "@type", "ItemList"
            ) and await has_key_value(json_content, "@type", "ListItem"):
                return json_content
        else:
            msg = "ItemList not available on this search page."
            logger.error(msg)
            raise ValueError(msg)

    @staticmethod
    async def get_ProductSummary(
        page_data: types.JSON,
    ) -> list[FlipkartSearchPageProductSummaryModel]:
        products = []
        for i in [
            i for v in page_data["pageDataV4"]["page"]["data"].values() for i in v
        ]:
            if await has_key_value(i, "slotType", "WIDGET") and await has_key_value(
                i, "type", "PRODUCT_SUMMARY"
            ):
                try:
                    product = FlipkartSearchPageProductSummaryModel(
                        dataId=i["dataId"],
                        parentId=i["parentId"],
                        elementId=i["elementId"],
                        **i["widget"]["data"]["products"][0]["productInfo"]["value"],
                    )
                    products.append(product)
                except (KeyError, IndexError) as e:
                    logger.error(e)
                    continue
        if not products:
            raise FlipkartSearchPageError("0 product parsed!")
        logger.info(f"Parsed {len(products)} products summary.")
        return products

    async def parse_all_ItemList(self) -> list[types.JSON]:
        html_pages = await self.get_html_pages()
        items = await asyncio.gather(*[self.get_ItemList(i) for i in html_pages])
        return [j for i in items for j in i]

    async def parse_all_PageData(self) -> list[types.JSON]:
        html_pages = await self.get_html_pages()
        items = await asyncio.gather(*[parse_flipkart_page_json(i) for i in html_pages])
        return items

    async def parse_all_ProductSummary(
        self,
    ) -> list[FlipkartSearchPageProductSummaryModel]:
        pages_data = await self.parse_all_PageData()
        items = await asyncio.gather(*[self.get_ProductSummary(i) for i in pages_data])
        products = [j for i in items for j in i]
        if not products:
            raise FlipkartSearchPageError("0 product parsed!")
        logger.info(f"Parsed total {len(products)} products summaries.")
        return products
