from fastapi.testclient import TestClient

from ecommerce.api.app import app

from ._utils import _RANDOM_PRODUCT_URL, TEST_PRODUCT_URLS

client = TestClient(app, "https://localhost:8000/flipkart/product")


def test_get_info():
    response = client.get(f"/?url={_RANDOM_PRODUCT_URL}")
    assert response.status_code == 200


def test_get_info_batch():
    response = client.post("/batch", json=TEST_PRODUCT_URLS)
    assert response.status_code == 200
