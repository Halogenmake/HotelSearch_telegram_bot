import requests
import string
from requests import Response
from config_data.config import URL_SEARCH, HEADERS


def request_city_search(text: str) -> Response:

    CITY_SEARCH = {
        'query': '',
        'locale': ''
    }

    for sym in text:
        if sym not in string.printable:
            CITY_SEARCH['locale'] = 'ru_RU'
            break
    else:
        CITY_SEARCH['locale'] = 'en_US'
    CITY_SEARCH['query'] = text
    response = requests.request('GET', URL_SEARCH, headers=HEADERS, params=CITY_SEARCH, timeout=15)
    return response
