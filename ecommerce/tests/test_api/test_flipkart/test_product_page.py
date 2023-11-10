from fastapi.testclient import TestClient

from ecommerce.api.app import app

from ._utils import _RANDOM_PRODUCT_URL, TEST_PRODUCT_URLS

client = TestClient(app, "https://localhost:8000/")

_ROOT_PATH = "/flipkart/product"


def test_get_info():
    response = client.get(f"{_ROOT_PATH}/?url={_RANDOM_PRODUCT_URL}")
    assert response.status_code == 200


def test_get_info_batch():
    response = client.post(f"{_ROOT_PATH}/batch", json=TEST_PRODUCT_URLS)
    assert response.status_code == 200
