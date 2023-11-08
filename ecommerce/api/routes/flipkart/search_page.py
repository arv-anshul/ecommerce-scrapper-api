from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ValidationError

from ecommerce.parser import get_PageData
from ecommerce.parser.flipkart import SEARCH_PAGE_CURL_PATH, FlipkartSearchPage
from ecommerce.parser.flipkart.search_page import FlipkartSearchPageError
from ecommerce.validator.flipkart.search_page import (
    FlipkartSearchPageProductSummaryModel,
)

search_page_router = APIRouter(prefix="/search", tags=["flipkart", "searchPage"])


class FlipkartSearchPageParams(BaseModel):
    params: dict[str, str]


@search_page_router.get("/")
async def search(q: str, page: int = 1) -> list[FlipkartSearchPageProductSummaryModel]:
    flipkart = FlipkartSearchPage(q, pages=[page], curl_fp=SEARCH_PAGE_CURL_PATH)
    html = await flipkart.get_html_pages()
    try:
        summary = await flipkart.get_ProductSummary(await get_PageData(html[0]))
    except FlipkartSearchPageError as e:
        raise HTTPException(204, detail={"message": e})
    return summary


@search_page_router.post("/")
async def search_with_params(
    q: str,
    params: FlipkartSearchPageParams = FlipkartSearchPageParams(params={"page": "1"}),
) -> list[FlipkartSearchPageProductSummaryModel]:
    flipkart = FlipkartSearchPage(
        q, curl_fp=SEARCH_PAGE_CURL_PATH, params=params.params
    )
    html = await flipkart.get_html_pages()
    try:
        summary = await flipkart.get_ProductSummary(await get_PageData(html[0]))
    except FlipkartSearchPageError as e:
        raise HTTPException(204, {"message": e})
    return summary


def _validate_pagination(from_page: int, to_page: int) -> None:
    error_msg = None
    if from_page < 1:
        error_msg = "'from_page' must be greater than 0."
    if from_page >= to_page:
        error_msg = "'from_page' must be smaller than 'to_page'"
    if error_msg:
        raise HTTPException(
            204,
            {
                "message": error_msg,
                "query": {"from_page": from_page, "to_page": to_page},
            },
        )


@search_page_router.get("/batch")
async def search_in_batch(
    q: str, from_page: int = 1, to_page: int = 5
) -> list[FlipkartSearchPageProductSummaryModel]:
    _validate_pagination(from_page, to_page)
    flipkart = FlipkartSearchPage(
        q, pages=range(from_page, to_page), curl_fp=SEARCH_PAGE_CURL_PATH
    )
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
    q: str, from_page: int, to_page: int, params: FlipkartSearchPageParams
) -> list[FlipkartSearchPageProductSummaryModel]:
    _validate_pagination(from_page, to_page)
    flipkart = FlipkartSearchPage(
        q,
        pages=range(from_page, to_page),
        curl_fp=SEARCH_PAGE_CURL_PATH,
        params=params.params,
    )
    try:
        summary = await flipkart.parse_all_ProductSummary()
    except (ValidationError, TypeError, KeyError) as e:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"message": e, "errorType": e.__class__.__name__},
        )
    return summary
