from fastapi import APIRouter, HTTPException

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
async def get_reviews(
    url: str, from_page: int = 1, to_page: int = 5
) -> list[FlipkartProductReviews]:
    flipkart = FlipkartReviewPage(url, range(from_page, to_page))
    reviews = await flipkart.parse_all_reviews()
    return reviews


@review_page_router.post("/")
async def get_reviews_with_params(
    from_page: int = 1,
    to_page: int = 5,
    data: dict = {
        "url": "",
        "params": DEFAULT_FLIPKART_REVIEW_PAGE_PARAMS,
    },
) -> list[FlipkartProductReviews]:
    try:
        url, params = data.values()
    except ValueError:
        raise HTTPException(422, {"message": "data must be only 'url' and 'params'."})
    if "page" in params:
        raise HTTPException(400, "params must not contains 'page' key.")
    flipkart = FlipkartReviewPage(url, range(from_page, to_page), params=params)
    reviews = await flipkart.parse_all_reviews()
    return reviews
