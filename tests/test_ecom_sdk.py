from ecom_sdk.ecom_sdk import EcomSDK
import responses
from responses import matchers


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
    assert stores[0]["id"] == 1
    assert stores[0]["name"] == "Lidl"