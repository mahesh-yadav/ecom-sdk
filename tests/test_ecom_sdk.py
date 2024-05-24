from ecom_sdk.ecom_sdk import EcomSDK
from ecom_sdk.models import Product, Store, EcomAPIConfig
import responses
from responses import matchers
import requests
import pytest


@pytest.fixture
def ecom_sdk_config():
    return EcomAPIConfig(api_url="https://api.example.com", api_key="1234567890")


def test_ecom_sdk_class(ecom_sdk_config):
    sdk = EcomSDK(ecom_sdk_config)
    assert sdk._api_url == ecom_sdk_config.api_url
    assert sdk._api_key == ecom_sdk_config.api_key


@responses.activate
def test_sdk_list_stores(ecom_sdk_config):
    responses.add(
        responses.GET,
        ecom_sdk_config.api_url + "/stores",
        status=200,
        json=[
            {"id": 1, "name": "Lidl", "products": 10},
            {"id": 2, "name": "Walmart", "products": 15},
        ],
        match=[matchers.header_matcher({"X-API-KEY": ecom_sdk_config.api_key})],
    )

    sdk = EcomSDK(ecom_sdk_config)
    stores = sdk.list_stores()

    assert len(stores) == 2
    assert stores[0].id == 1
    assert stores[0].name == "Lidl"
    assert isinstance(stores[0], Store)


@responses.activate
def test_sdk_list_stores_connection_error(ecom_sdk_config):
    responses.add(
        responses.GET,
        ecom_sdk_config.api_url + "/stores",
        body=requests.exceptions.ConnectionError(),
    )

    sdk = EcomSDK(ecom_sdk_config)

    with pytest.raises(ValueError) as exec_info:
        sdk.list_stores()

    assert "Connection error" in str(exec_info.value)


@responses.activate
def test_sdk_list_stores_authentication_error(ecom_sdk_config):
    responses.add(
        responses.GET,
        ecom_sdk_config.api_url + "/stores",
        status=403,
    )

    sdk = EcomSDK(ecom_sdk_config)

    with pytest.raises(ValueError) as exec_info:
        sdk.list_stores()

    assert "Authentication error" in str(exec_info.value)


@responses.activate
def test_sdk_list_products_sort_by_price_desc(ecom_sdk_config):
    store_id = 1
    responses.add(
        responses.GET,
        ecom_sdk_config.api_url + f"/stores/{store_id}/products",
        status=200,
        json=[
            {"id": 1, "price": 100, "name": "Banana"},
            {"id": 2, "price": 200, "name": "Apple"},
        ],
        match=[matchers.header_matcher({"X-API-KEY": ecom_sdk_config.api_key})],
    )

    sdk = EcomSDK(ecom_sdk_config)
    products = sdk.list_products(
        store_id,
        sort_by=EcomSDK.ProductSortBy.PRICE,
        sort_order=EcomSDK.ProductSortOrder.DESC,
    )

    assert len(products) == 2
    assert products[0].id == 1
    assert products[0].price == 100
    assert products[1].name == "Apple"
    assert isinstance(products[1], Product)
