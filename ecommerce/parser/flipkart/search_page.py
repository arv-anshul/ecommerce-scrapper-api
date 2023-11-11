import asyncio
import urllib.parse
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from ecommerce import types
from ecommerce.core import io
from ecommerce.core.errors import SearchPageError
from ecommerce.logger import get_logger
from ecommerce.parser import Pagination, get_html_pages, has_key_value
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.parser.search_page import BaseSearchPageHTMLParser
from ecommerce.validator.flipkart import (
    FlipkartSearchPageItemList,
    FlipkartSearchPageProductSummaryModel,
)

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

    async def get_html_pages(
        self, client: Optional[httpx.AsyncClient] = None
    ) -> list[str]:
        responses = await get_html_pages(self.urls, self.requests_kws, client)
        return [v for i in responses for v in i.values()]

    @staticmethod
    async def get_ItemList(html: str) -> list[FlipkartSearchPageItemList]:
        soup = BeautifulSoup(html, "html.parser")
        page_data = await parse_flipkart_page_json(html)
        product_ids = page_data["pageDataV4"]["browseMetadata"]["productList"]

        async def get_product_details(pid: str) -> dict[str, Optional[str]]:
            product_card = soup.select_one(f"div[data-id={pid!r}]")
            if product_card is None:
                return {"pid": pid}
            url: str = product_card.div.a["href"]  # type: ignore
            img_tag = product_card.select_one("img[loading]")
            return {
                "pid": pid,
                "name": img_tag["alt"] if img_tag else None,  # type: ignore
                "url": "https://flipkart.com" + url.split("?")[0] + f"?pid={pid}",
            }

        products = await asyncio.gather(*[get_product_details(i) for i in product_ids])
        return [FlipkartSearchPageItemList(**i) for i in products]

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

    async def parse_all_ItemList(self) -> list[FlipkartSearchPageItemList]:
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
