import asyncio
from typing import Optional

import httpx

from ecommerce import types
from ecommerce.core import io
from ecommerce.logger import get_logger
from ecommerce.parser import BaseProductPageHTMLParser, fetch_page, has_key_value
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.validator.flipkart.product_page import (
    FlipkartProductInfo,
    _ProductOffers,
    _ProductSchema,
    _ProductSpecifications,
)

logger = get_logger(__name__)
PRODUCT_PAGE_CURL_PATH = "configs/curl/flipkart.productPage"


class FlipkartProductPage(BaseProductPageHTMLParser):
    def __init__(
        self,
        url: str,
        params: Optional[types.URLParams] = None,
    ) -> None:
        self.url = url
        self.__cached_page: dict[str, str] = {}

        self.requests_kws = io.get_curl_command(PRODUCT_PAGE_CURL_PATH)
        self.requests_kws.update({"params": params}) if params else ...

    @property
    def get_cached_html_pages(self) -> Optional[dict[str, str]]:
        return self.__cached_page if self.__cached_page else None

    async def get_html_page(self, client: Optional[httpx.AsyncClient] = None) -> str:
        if self.url in self.__cached_page:
            logger.info(f"Returning cached page of url {self.url!r}")
            return self.__cached_page[self.url]

        # If client is provide then just make request with the url
        if client:
            return await fetch_page(self.url, client)

        async with httpx.AsyncClient(
            **self.requests_kws,
            follow_redirects=True,
            timeout=3,
        ) as client:
            html = await fetch_page(self.url, client)
            return html

    @staticmethod
    async def get_ProductInfo(html: str) -> FlipkartProductInfo:
        page_data = await parse_flipkart_page_json(html)
        schema, offers, specs, variants = None, None, None, None

        # Extract Product Schema Data
        schema_data = page_data["seoMeta"]["metadata"]["schema"]
        for i in schema_data:
            if schema is None and await has_key_value(i, "@type", "Product"):
                schema = _ProductSchema(**i)
                logger.info(f"Parsed schemas for {schema.name!r}")

        # Extract Offers, Specs, Variants Data
        for i in [
            i for v in page_data["pageDataV4"]["page"]["data"].values() for i in v
        ]:
            if offers is None and await has_key_value(i, "type", "OfferSummaryV3Group"):
                offers = [
                    _ProductOffers(**j["value"])
                    for j in i["widget"]["data"]["offerGroups"][0][
                        "renderableComponents"
                    ]
                ]
                logger.info(f"Parsed {len(offers)} offers.")
            if specs is None and await has_key_value(
                i, "type", "ProductSpecificationValue"
            ):
                specs = [
                    _ProductSpecifications(specifications=j["value"]["attributes"])
                    for j in i["widget"]["data"]["renderableComponents"]
                ]
                logger.info(f"Parsed {len(specs)} specs.")
            if (
                variants is None
                and await has_key_value(i, "type", "ProductSwatchValue")
                and await has_key_value(i, "swatchComponent")
            ):
                variants_list = i["widget"]["data"]["swatchComponent"]["value"][
                    "attributeOptions"
                ]
                variants = {
                    f"variant_{idx}": [v["value"] for v in item]
                    for idx, item in enumerate(variants_list, 1)
                }
                logger.info(f"Parsed {len(variants)} variants.")

        logger.info(f"Fetched ProductInfo of {schema.name!r}.") if schema else ...
        return FlipkartProductInfo(
            schemas=schema, offers=offers, specs=specs, variants=variants
        )

    @staticmethod
    async def batch_products_info(
        client: httpx.AsyncClient, *urls: str
    ) -> list[FlipkartProductInfo]:
        tasks = []
        for url in urls:
            flipkart = FlipkartProductPage(url)
            tasks.append(flipkart.get_html_page(client))
        pages = await asyncio.gather(*tasks)
        infos = asyncio.gather(*[FlipkartProductPage.get_ProductInfo(i) for i in pages])
        return await infos
