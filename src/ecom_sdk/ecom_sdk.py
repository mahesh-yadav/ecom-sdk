import requests


HTTP_REQUEST_TIMEOUT = 10


class EcomSDK:
    def __init__(self, api_url, api_key):
        self._api_url = api_url
        self._api_key = api_key

    def list_stores(self):
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

        return response.json()