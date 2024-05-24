import requests
from enum import Enum
from .models import Product, Store


HTTP_REQUEST_TIMEOUT = 10


class EcomSDK:

    class ProductSortBy(str, Enum):
        PRICE = "price"
        Quantity = "quantity"


    class ProductSortOrder(str, Enum):
        DESC = "desc"
        ASC = "asc"

    def __init__(self, api_url, api_key):
        self._api_url = api_url
        self._api_key = api_key

    def list_stores(self) -> list[Store]:
        try:
            response = requests.get(
                self._api_url + "/stores",
                headers={"X-API-KEY": self._api_key},
                timeout=HTTP_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ValueError("Connection error, check `EcomSDK._api_url` is set correctly") from e
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise ValueError("Authentication error, check `EcomSDK._api_key` is set correctly") from e
            else:
                raise

        return [Store(**store) for store in response.json()]
    
    def list_products(self, store_id, sort_by=ProductSortBy.PRICE, sort_order=ProductSortOrder.ASC) -> list[Product]:
        try:
            response = requests.get(
                self._api_url + f"/stores/{store_id}/products",
                headers={"X-API-KEY": self._api_key},
                params={"sortBy": sort_by, "sortOrder": sort_order},
                timeout=HTTP_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ValueError("Connection error, check `EcomSDK._api_url` is set correctly") from e
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise ValueError("Authentication error, check `EcomSDK._api_key` is set correctly") from e
            else:
                raise

        return [Product(**product) for product in response.json()]