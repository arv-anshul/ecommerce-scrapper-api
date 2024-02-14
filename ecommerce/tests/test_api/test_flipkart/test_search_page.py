import pytest
from fastapi.testclient import TestClient

from ecommerce.api.app import app
from ecommerce.api.routes.flipkart.search_page import (
    DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
)

from ._utils import _RANDOM_SEARCH_QUERY

client = TestClient(app, base_url="https://localhost:8000/flipkart/search")


def test_search():
    response = client.get(f"/?q={_RANDOM_SEARCH_QUERY}")
    assert response.status_code == 200


def test_search_with_params():
    response = client.post(
        f"/?q={_RANDOM_SEARCH_QUERY}",
        json=DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
    )
    assert response.status_code == 200


def test_search_batch():
    response = client.get(f"/batch/?q={_RANDOM_SEARCH_QUERY}&to_page=3")
    assert response.status_code == 200


def test_search_batch_with_params():
    response = client.post(
        f"/batch/?q={_RANDOM_SEARCH_QUERY}&to_page=3",
        json=DEFAULT_FLIPKART_SEARCH_PAGE_PARAMS,
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    ["route", "from_page", "to_page"],
    [
        ("/", 1, 3),
        ("/batch", 2, 3),
    ],
)
def test_search_batch_with_invalid_params(
    route: str,
    from_page: int,
    to_page: int,
):
    response = client.post(
        f"{route}?q={_RANDOM_SEARCH_QUERY}&from_page={from_page}&to_page={to_page}",
        json={"page": 1},
    )
    assert response.status_code == 400
    assert response.json()["message"] == "params must not contains 'page' key."


@pytest.mark.parametrize(
    ["from_page", "status_code", "error_message"],
    [
        (-1, 400, "Pages must be positive."),
        (0, 400, "0 is prohibited."),
    ],
)
def test_search_batch_with_invalid_pages(
    from_page: int,
    status_code: int,
    error_message: str,
):
    response = client.get(f"/batch/?q={_RANDOM_SEARCH_QUERY}&from_page={from_page}")
    data = response.json()
    assert response.status_code == status_code
    assert data["message"] == error_message
