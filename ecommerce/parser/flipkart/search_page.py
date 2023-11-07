import asyncio
import json
import urllib.parse
import warnings
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from ecommerce import constants as C
from ecommerce import types
from ecommerce.core import io
from ecommerce.logger import get_logger
from ecommerce.parser import Pagination, fetch_page, get_PageData, has_key_value
from ecommerce.parser.search_page import BaseSearchPageHTMLParser
from ecommerce.validator.flipkart import FlipkartSearchPageProductSummaryModel

logger = get_logger(__name__)


class FlipkartSearchPage(BaseSearchPageHTMLParser):
    def __init__(
        self,
        search_query: str,
        *,
        curl_fp: Optional[types.PathLike] = C.SEARCH_PAGE_CURL_PATH,
        params: Optional[types.URLParams] = None,
        pages: types.PagesLike = range(1, 6),
    ):
        self.search_query = search_query
        self.pages = Pagination(pages)
        self.__cached_html_pages = {}
        self._import_requests_kwargs(curl_fp, params)

    def _import_requests_kwargs(
        self,
        curl_fp: Optional[types.PathLike],
        params: Optional[types.URLParams],
    ) -> None:
        # Set requests_kws for better http request
        if curl_fp:
            __kwargs = io.get_requests_kwargs(curl_fp)
            self.requests_kws = __kwargs if __kwargs else {}
        else:
            warnings.warn(
                "Please provide curl command for making requests. "
                "This may cause error in future.",
                FutureWarning,
            )

        # Update url params if specified
        if params:
            self.requests_kws.update({"params": params})

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
            if has_key_value(json_content, "@type", "ItemList") and has_key_value(
                json_content, "@type", "ListItem"
            ):
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
            region_validation = has_key_value(
                i, "slotType", "WIDGET"
            ) and has_key_value(i, "type", "PRODUCT_SUMMARY")
            if region_validation is True:
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
        logger.info(f"Parsed {len(products)} products summary.")
        return products

    async def parse_all_ItemList(
        self,
        only_cached_pages: bool = False,
    ) -> list[types.JSON]:
        html_pages = (
            self.get_all_cached_html_pages.values()
            if only_cached_pages
            else await self.get_html_pages()
        )
        items = await asyncio.gather(*[self.get_ItemList(i) for i in html_pages])
        return [j for i in items for j in i]

    async def parse_all_PageData(
        self,
        only_cached_pages: bool = False,
    ) -> list[types.JSON]:
        html_pages = (
            self.get_all_cached_html_pages.values()
            if only_cached_pages
            else await self.get_html_pages()
        )
        items = await asyncio.gather(*[get_PageData(i) for i in html_pages])
        return items

    async def parse_all_ProductSummary(
        self,
        only_cached_pages: bool = False,
    ) -> list[FlipkartSearchPageProductSummaryModel]:
        pages_data = await self.parse_all_PageData(only_cached_pages)
        items = await asyncio.gather(*[self.get_ProductSummary(i) for i in pages_data])
        products = [j for i in items for j in i]
        logger.info(f"Parsed total {len(products)} products summaries.")
        return products
