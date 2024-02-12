import asyncio
import urllib.parse

import httpx

from ecommerce import parser, types
from ecommerce.core import io
from ecommerce.core.errors import ReviewPageError
from ecommerce.logger import get_logger
from ecommerce.parser import BaseReviewPageHTMLParser, Pagination, get_html_pages
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.validator.flipkart import FlipkartProductReviews
from ecommerce.validator.flipkart.review_page import _ProductDetails

FLIPKART_REVIEW_PAGE_CURL_PATH = "configs/curl/flipkart.reviewPage"
logger = get_logger(__name__)


class FlipkartReviewPageError(ReviewPageError):
    """Exception specific to Flipkart's ReviewPages."""


class FlipkartReviewPage(BaseReviewPageHTMLParser):
    def __init__(
        self,
        product_url: str,
        pages: types.PagesLike = range(1, 5),
        params: types.URLParams | None = None,
    ) -> None:
        self._product_url = product_url
        self.pages = Pagination(pages)

        self.requests_kws = io.get_curl_command(FLIPKART_REVIEW_PAGE_CURL_PATH)
        self.requests_kws.update({"params": params}) if params else ...

    @property
    def urls(self) -> set[str]:
        url = self._product_url.replace("/p/", "/product-reviews/")
        return {
            urllib.parse.quote(
                f"{url}&page={page}&sortOrder=MOST_HELPFUL",
                safe="/?:=&",
            )
            for page in self.pages
        }

    async def get_html_pages(
        self, client: httpx.AsyncClient | None = None
    ) -> list[str]:
        responses = await get_html_pages(self.urls, self.requests_kws, client)
        return [v for i in responses for v in i.values()]

    @staticmethod
    async def get_reviews(page_data: types.JSON) -> list[FlipkartProductReviews]:
        reviews = []
        product_details = None

        for i in [
            i for v in page_data["pageDataV4"]["page"]["data"].values() for i in v
        ]:
            if await parser.has_key_value(
                i, "type", "REVIEWS"
            ) and await parser.has_key_value(i, "type", "ProductReviewValue"):
                reviews.append(i["widget"]["data"]["renderableComponents"][0]["value"])
            if product_details is None and await parser.has_key_value(
                i, "type", "ProductSummaryValue"
            ):
                product_details = _ProductDetails(
                    **i["widget"]["data"]["product"]["value"]
                )

        if product_details is None:
            raise FlipkartReviewPageError(
                "ProductDetail is not available on this review page."
            )

        return [
            FlipkartProductReviews(**i, productDetails=product_details) for i in reviews
        ]

    async def parse_all_reviews(self) -> list[FlipkartProductReviews]:
        pages = await self.get_html_pages()
        pages_data = await asyncio.gather(*[parse_flipkart_page_json(i) for i in pages])
        reviews = await asyncio.gather(*[self.get_reviews(i) for i in pages_data])
        reviews = [j for i in reviews for j in i]
        logger.info(f"{len(reviews)} reviews fetched.")
        return reviews
