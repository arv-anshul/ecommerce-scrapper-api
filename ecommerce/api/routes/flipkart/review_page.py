from fastapi import APIRouter

from ecommerce.api import APIExceptionResponder
from ecommerce.parser.flipkart import FlipkartReviewPage
from ecommerce.validator.flipkart import FlipkartProductReviews

review_page_router = APIRouter(
    prefix="/product/reviews", tags=["flipkart", "reviewPage"]
)
DEFAULT_FLIPKART_REVIEW_PAGE_PARAMS = {
    "aid": "overall",
    "certifiedBuyer": "true",
    "sortOrder": "MOST_HELPFUL",
}


@review_page_router.get("/")
@APIExceptionResponder.better_api_error_response
async def get_reviews(
    url: str, from_page: int = 1, to_page: int = 5
) -> list[FlipkartProductReviews]:
    flipkart = FlipkartReviewPage(url, range(from_page, to_page))
    reviews = await flipkart.parse_all_reviews()
    return reviews


@review_page_router.post("/")
@APIExceptionResponder.better_api_error_response
async def get_reviews_with_params(
    from_page: int = 1,
    to_page: int = 5,
    data: dict = {  # noqa: B006
        "url": "",
        "params": DEFAULT_FLIPKART_REVIEW_PAGE_PARAMS,
    },
) -> list[FlipkartProductReviews]:
    try:
        url, params = data.values()
    except ValueError:
        APIExceptionResponder.update(422)
        raise ValueError("Data must have only 'url' and 'params' keys.") from None
    if "page" in params:
        raise ValueError("Params data must not contain 'page' key.")
    flipkart = FlipkartReviewPage(url, range(from_page, to_page), params=params)
    reviews = await flipkart.parse_all_reviews()
    return reviews
