import httpx
from fastapi import APIRouter, HTTPException

from ecommerce.core import io
from ecommerce.parser.flipkart import (
    PRODUCT_PAGE_CURL_PATH,
    FlipkartProductPage,
    fetch_multiple_products_info,
)
from ecommerce.validator.flipkart import FlipkartProductInfo

product_page_router = APIRouter(prefix="/product", tags=["flipkart", "productPage"])


@product_page_router.get("/")
async def get_info(url: str) -> FlipkartProductInfo:
    flipkart = FlipkartProductPage(url, curl_fp=PRODUCT_PAGE_CURL_PATH)
    html = await flipkart.get_html_page()
    info = await flipkart.get_ProductInfo(html)
    return info


@product_page_router.post("/batch")
async def get_info_in_batch(urls: list[str]) -> list[FlipkartProductInfo]:
    curl_fp = "configs/curl/flipkart.productPage"
    requests_kws = io.get_requests_kwargs(curl_fp)
    if requests_kws is None:
        raise HTTPException(
            404,
            detail={
                "message": "requests kwargs is None.",
                "path": curl_fp,
            },
        )
    async with httpx.AsyncClient(**requests_kws) as client:
        products = await fetch_multiple_products_info(client, *urls)
        return products
