from fastapi import APIRouter

from ecommerce.api import APIExceptionResponder
from ecommerce.parser.flipkart import FlipkartSearchPage
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.validator.flipkart import (
    FlipkartSearchPageItemList,
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
    APIExceptionResponder.update(204)
    summary = await flipkart.get_ProductSummary(await parse_flipkart_page_json(html[0]))
    return summary


@search_page_router.post("/")
@APIExceptionResponder.better_api_error_response
async def search_with_params(
    q: str,
    from_page: int = 1,
    to_page: int = 5,
    params: dict = DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
) -> list[FlipkartSearchPageProductSummaryModel]:
    if "page" in params:
        raise ValueError("params must not contains 'page' key.")
    flipkart = FlipkartSearchPage(q, pages=range(from_page, to_page), params=params)
    html = await flipkart.get_html_pages()
    APIExceptionResponder.update(204)
    summary = await flipkart.get_ProductSummary(await parse_flipkart_page_json(html[0]))
    return summary


@search_page_router.get("/batch")
@APIExceptionResponder.better_api_error_response
async def search_in_batch(
    q: str, from_page: int = 1, to_page: int = 5
) -> list[FlipkartSearchPageProductSummaryModel]:
    flipkart = FlipkartSearchPage(q, pages=range(from_page, to_page))
    APIExceptionResponder.update(422)
    summary = await flipkart.parse_all_ProductSummary()
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
    APIExceptionResponder.update(422)
    summary = await flipkart.parse_all_ProductSummary()
    return summary


@search_page_router.get("/item-list")
@APIExceptionResponder.better_api_error_response
async def get_item_list_from_search_page(
    q: str,
    from_page: int = 1,
    to_page: int = 5,
) -> list[FlipkartSearchPageItemList]:
    flipkart = FlipkartSearchPage(q, range(from_page, to_page))
    APIExceptionResponder.update(422)
    items = await flipkart.parse_all_ItemList()
    return items


@search_page_router.post("/item-list")
@APIExceptionResponder.better_api_error_response
async def get_item_list_from_search_page_with_params(
    q: str,
    from_page: int = 1,
    to_page: int = 5,
    params: dict = DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
) -> list[FlipkartSearchPageItemList]:
    flipkart = FlipkartSearchPage(q, range(from_page, to_page), params)
    APIExceptionResponder.update(422)
    items = await flipkart.parse_all_ItemList()
    return items
