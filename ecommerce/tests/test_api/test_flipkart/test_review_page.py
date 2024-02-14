from fastapi.testclient import TestClient

from ecommerce.api.app import app
from ecommerce.api.routes.flipkart.review_page import (
    DEFAULT_FLIPKART_REVIEW_PAGE_PARAMS,
)

from ._utils import _RANDOM_PRODUCT_URL

client = TestClient(app, "https://localhost:8000/flipkart/product/reviews")


def test_get_reviews():
    response = client.get(f"/?url={_RANDOM_PRODUCT_URL}")
    assert response.status_code == 200


def test_get_reviews_with_params():
    response = client.post(
        "/?to_page=3",
        json={
            "url": _RANDOM_PRODUCT_URL,
            "params": DEFAULT_FLIPKART_REVIEW_PAGE_PARAMS,
        },
    )
    assert response.status_code == 200


def test_get_reviews_with_invalid_params():
    response = client.post(
        "/",
        json={"url": "https://www.flipkart.com/bad-url", "params": {"page": 1}},
    )
    assert response.status_code == 400
    data = response.json()
    assert "Params data must not contain 'page' key." in data["message"]
