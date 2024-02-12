from fastapi.testclient import TestClient

from ecommerce.api.app import app
from ecommerce.api.routes.flipkart.search_page import (
    DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
)

from ._utils import _RANDOM_SEARCH_QUERY

client = TestClient(app, base_url="https://localhost:8000")

_ROOT_PATH = "/flipkart/search"


def test_search():
    response = client.get(f"{_ROOT_PATH}/?q={_RANDOM_SEARCH_QUERY}")
    assert response.status_code == 200


def test_search_with_params():
    response = client.post(
        f"{_ROOT_PATH}/?q={_RANDOM_SEARCH_QUERY}",
        json=DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
    )
    assert response.status_code == 200


def test_search_batch():
    response = client.get(f"{_ROOT_PATH}/batch/?q={_RANDOM_SEARCH_QUERY}&to_page=3")
    assert response.status_code == 200


def test_search_batch_with_params():
    response = client.post(
        f"{_ROOT_PATH}/batch/?q={_RANDOM_SEARCH_QUERY}&to_page=3",
        json=DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
    )
    assert response.status_code == 200


def test_search_with_invalid_params():
    response = client.post(
        f"{_ROOT_PATH}/?q={_RANDOM_SEARCH_QUERY}&to_page=3",
        json={"page": 1},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "params must not contains 'page' key."


def test_search_batch_with_invalid_params():
    response = client.post(
        f"{_ROOT_PATH}/batch/?q={_RANDOM_SEARCH_QUERY}&from_page=1&to_page=3",
        json={"page": 1},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "params must not contains 'page' key."


def test_search_batch_with_invalid_pages():
    response = client.get(f"{_ROOT_PATH}/batch/?q={_RANDOM_SEARCH_QUERY}&from_page=-1")
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Pages must be positive."

    response = client.get(f"{_ROOT_PATH}/batch/?q={_RANDOM_SEARCH_QUERY}&from_page=0")
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "0 is prohibited."
