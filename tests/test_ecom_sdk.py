from ecom_sdk.ecom_sdk import EcomSDK
from ecom_sdk.models import Product, Store
import responses
from responses import matchers
import requests
import pytest


API_URL = "https://api.example.com"
API_KEY = "1234567890"


def test_ecom_sdk_class():
    sdk = EcomSDK(API_URL, API_KEY)
    assert sdk._api_url == API_URL
    assert sdk._api_key == API_KEY


@responses.activate
def test_sdk_list_stores():
    responses.add(
        responses.GET,
        API_URL + "/stores",
        status=200,
        json=[
            {"id": 1, "name": "Lidl", "products": 10},
            {"id": 2, "name": "Walmart", "products": 15},
        ],
        match=[matchers.header_matcher({"X-API-KEY": API_KEY})]
    )

    sdk = EcomSDK(API_URL, API_KEY)
    stores = sdk.list_stores()

    assert len(stores) == 2
    assert stores[0].id == 1
    assert stores[0].name == "Lidl"
    assert isinstance(stores[0], Store)


@responses.activate
def test_sdk_list_stores_connection_error():
    responses.add(
        responses.GET,
        API_URL + "/stores",
        body=requests.exceptions.ConnectionError(),
    )

    sdk = EcomSDK(API_URL, API_KEY)

    with pytest.raises(ValueError) as exec_info:
        sdk.list_stores()

    assert "Connection error" in str(exec_info.value)


@responses.activate
def test_sdk_list_stores_authentication_error():
    responses.add(
        responses.GET,
        API_URL + "/stores",
        status=403,
    )

    sdk = EcomSDK(API_URL, API_KEY)

    with pytest.raises(ValueError) as exec_info:
        sdk.list_stores()

    assert "Authentication error" in str(exec_info.value)


@responses.activate
def test_sdk_list_products_sort_by_price_desc():
    store_id = 1
    responses.add(
        responses.GET,
        API_URL + f"/stores/{store_id}/products",
        status=200,
        json=[
            {"id": 1, "price": 100, "name": "Banana"},
            {"id": 2, "price": 200, "name": "Apple"},
        ],
        match=[matchers.header_matcher({"X-API-KEY": API_KEY})]
    )

    sdk = EcomSDK(API_URL, API_KEY)
    products = sdk.list_products(store_id, sort_by=EcomSDK.ProductSortBy.PRICE, sort_order=EcomSDK.ProductSortOrder.DESC)

    assert len(products) == 2
    assert products[0].id == 1
    assert products[0].price == 100
    assert products[1].name == "Apple"
    assert isinstance(products[1], Product)
