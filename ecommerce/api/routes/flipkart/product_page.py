import httpx
from fastapi import APIRouter

from ecommerce.core import io
from ecommerce.parser.flipkart import PRODUCT_PAGE_CURL_PATH, FlipkartProductPage
from ecommerce.validator.flipkart import FlipkartProductInfo

product_page_router = APIRouter(prefix="/product", tags=["flipkart", "productPage"])


@product_page_router.get("/")
async def get_info(url: str) -> FlipkartProductInfo:
    flipkart = FlipkartProductPage(url)
    html = await flipkart.get_html_page()
    info = await flipkart.get_ProductInfo(html)
    return info


@product_page_router.post("/batch")
async def get_info_in_batch(urls: list[str]) -> list[FlipkartProductInfo]:
    requests_kws = io.get_curl_command(PRODUCT_PAGE_CURL_PATH)
    async with httpx.AsyncClient(**requests_kws) as client:
        products = await FlipkartProductPage.batch_products_info(client, *urls)
        return products
