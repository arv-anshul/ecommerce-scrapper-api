from fastapi import APIRouter

from ecommerce.api import APIExceptionResponder
from ecommerce.parser.flipkart import FlipkartSearchPage
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.validator.flipkart.search_page import (
    FlipkartSearchPageProductSummaryModel,
)

search_page_router = APIRouter(prefix="/search", tags=["flipkart", "searchPage"])
DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS = {
    "sort": "relevance",
    "p[]'[0]": "facets.price_range.from=Min",
    "p[]'[1]": "facets.price_range.to=Max",
}


@search_page_router.get("/")
@APIExceptionResponder.better_api_error_response
async def search(q: str, page: int = 1) -> list[FlipkartSearchPageProductSummaryModel]:
    flipkart = FlipkartSearchPage(q, pages=[page])
    html = await flipkart.get_html_pages()
    APIExceptionResponder.update_variables(204)
    summary = await flipkart.get_ProductSummary(await parse_flipkart_page_json(html[0]))
    APIExceptionResponder.reset_variables()
    return summary


@search_page_router.post("/")
@APIExceptionResponder.better_api_error_response
async def search_with_params(
    q: str,
    params: dict = DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
) -> list[FlipkartSearchPageProductSummaryModel]:
    if "page" in params:
        raise ValueError("params must not contains 'page' key.")
    flipkart = FlipkartSearchPage(q, params=params)
    html = await flipkart.get_html_pages()
    APIExceptionResponder.update_variables(204)
    summary = await flipkart.get_ProductSummary(await parse_flipkart_page_json(html[0]))
    APIExceptionResponder.reset_variables()
    return summary


@search_page_router.get("/batch")
@APIExceptionResponder.better_api_error_response
async def search_in_batch(
    q: str, from_page: int = 1, to_page: int = 5
) -> list[FlipkartSearchPageProductSummaryModel]:
    flipkart = FlipkartSearchPage(q, pages=range(from_page, to_page))
    APIExceptionResponder.update_variables(422)
    summary = await flipkart.parse_all_ProductSummary()
    APIExceptionResponder.reset_variables()
    return summary


@search_page_router.post("/batch")
@APIExceptionResponder.better_api_error_response
async def search_in_batch_with_params(
    q: str,
    from_page: int = 1,
    to_page: int = 5,
    params: dict = DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
) -> list[FlipkartSearchPageProductSummaryModel]:
    if "page" in params:
        raise ValueError("params must not contains 'page' key.")
    flipkart = FlipkartSearchPage(q, pages=range(from_page, to_page), params=params)
    APIExceptionResponder.update_variables(422)
    summary = await flipkart.parse_all_ProductSummary()
    APIExceptionResponder.reset_variables()
    return summary
