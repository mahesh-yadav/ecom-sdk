import requests


HTTP_REQUEST_TIMEOUT = 10


class EcomSDK:
    def __init__(self, api_url, api_key):
        self._api_url = api_url
        self._api_key = api_key

    def list_stores(self):
        response = requests.get(
            self._api_url + "/stores",
            headers={"X-API-KEY": self._api_key},
            timeout=HTTP_REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Invalid response status code: " + str(response.status_code))
        