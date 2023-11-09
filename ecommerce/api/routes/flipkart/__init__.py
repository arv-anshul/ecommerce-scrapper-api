import os

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
            "reviewPage": os.path.exists("configs/curl/flipkart.reviewPage"),
            "searchPage": os.path.exists("configs/curl/flipkart.searchPage"),
            "productPage": os.path.exists("configs/curl/flipkart.productPage"),
        },
    }


flipkart_router.include_router(search_page_router)
flipkart_router.include_router(product_page_router)
flipkart_router.include_router(review_page_router)
