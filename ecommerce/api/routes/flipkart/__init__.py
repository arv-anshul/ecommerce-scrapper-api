from pathlib import Path

from fastapi import APIRouter

from ecommerce.logger import get_logger

from .product_page import product_page_router
from .review_page import review_page_router
from .search_page import search_page_router

logger = get_logger(__name__)


flipkart_router = APIRouter(prefix="/flipkart", tags=["flipkart"])


@flipkart_router.get("/")
async def root():
    return {
        "running": True,
        "curl_commands": {
            "reviewPage": Path("configs/curl/flipkart.reviewPage").exists(),
            "searchPage": Path("configs/curl/flipkart.searchPage").exists(),
            "productPage": Path("configs/curl/flipkart.productPage").exists(),
        },
    }


flipkart_router.include_router(search_page_router)
flipkart_router.include_router(product_page_router)
flipkart_router.include_router(review_page_router)
