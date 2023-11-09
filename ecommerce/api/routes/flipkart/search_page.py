from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from ecommerce.core.errors import PaginationError
from ecommerce.parser.flipkart import FlipkartSearchPage
from ecommerce.parser.flipkart._utils import parse_flipkart_page_json
from ecommerce.parser.flipkart.search_page import FlipkartSearchPageError
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
async def search(q: str, page: int = 1) -> list[FlipkartSearchPageProductSummaryModel]:
    try:
        flipkart = FlipkartSearchPage(q, pages=[page])
    except PaginationError as e:
        raise HTTPException(400, {"message": str(e), "errorType": e.__class__.__name__})
    html = await flipkart.get_html_pages()
    try:
        summary = await flipkart.get_ProductSummary(
            await parse_flipkart_page_json(html[0])
        )
    except FlipkartSearchPageError as e:
        raise HTTPException(
            204, detail={"message": e, "errorType": e.__class__.__name__}
        )
    return summary


@search_page_router.post("/")
async def search_with_params(
    q: str,
    params: dict = DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
) -> list[FlipkartSearchPageProductSummaryModel]:
    if "page" in params:
        raise HTTPException(400, {"message": "params must not contains 'page' key."})
    try:
        flipkart = FlipkartSearchPage(q, params=params)
    except PaginationError as e:
        raise HTTPException(400, {"message": str(e), "errorType": e.__class__.__name__})
    html = await flipkart.get_html_pages()
    try:
        summary = await flipkart.get_ProductSummary(
            await parse_flipkart_page_json(html[0])
        )
    except FlipkartSearchPageError as e:
        raise HTTPException(204, {"message": e, "errorType": e.__class__.__name__})
    return summary


@search_page_router.get("/batch")
async def search_in_batch(
    q: str, from_page: int = 1, to_page: int = 5
) -> list[FlipkartSearchPageProductSummaryModel]:
    try:
        flipkart = FlipkartSearchPage(q, pages=range(from_page, to_page))
    except PaginationError as e:
        raise HTTPException(400, {"message": str(e), "errorType": e.__class__.__name__})
    try:
        summary = await flipkart.parse_all_ProductSummary()
    except (ValidationError, TypeError, KeyError) as e:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"message": e, "errorType": e.__class__.__name__},
        )
    return summary


@search_page_router.post("/batch")
async def search_in_batch_with_params(
    q: str,
    from_page: int,
    to_page: int,
    params: dict = DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
) -> list[FlipkartSearchPageProductSummaryModel]:
    if "page" in params:
        raise HTTPException(400, {"message": "params must not contains 'page' key."})
    try:
        flipkart = FlipkartSearchPage(q, pages=range(from_page, to_page), params=params)
    except PaginationError as e:
        raise HTTPException(400, {"message": str(e), "errorType": e.__class__.__name__})
    try:
        summary = await flipkart.parse_all_ProductSummary()
    except (ValidationError, TypeError, KeyError) as e:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"message": e, "errorType": e.__class__.__name__},
        )
    return summary
