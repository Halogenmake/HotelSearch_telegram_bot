"""
Пакет, содержащий необходимые функции запросов по API.
"""
from typing import Any

import requests
from config_data.config import HEADERS_GET, HEADERS_POST

def api_request(method_endswith: str, params: dict, method_type: str) -> Any | None:
    url = f'https://hotels4.p.rapidapi.com/{method_endswith}'

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            url=url,
            params=params
        )


def get_request(url, params):
    try:
        response = requests.get(
            url,
            headers=HEADERS_GET,
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            return ''

    except TimeoutError:
        return ''


def post_request(url, params):
    try:
        response = requests.post(
            url,
            headers=HEADERS_POST,
            json=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.text
        else:
            return ''

    except TimeoutError:
        return ''
