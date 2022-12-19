"""
Пакет, содержащий необходимые функции запросов по API.
"""
import requests
from config_data.config import HEADERS_GET, HEADERS_POST


def api_request(method_endswith: str, params: dict, method_type: str) -> str | None:
    """
    Универсальная функция работы с запросами. В зависимости от метода запроса, вызывает одну из дочерних функций
    :params method_endswith: str - окончание url-запроса к API
    :params params: dict - словарь, содержащий параметры запроса
    :params method_type: str - метод GET или POST

    :return текст запроса
    """

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


def get_request(url: str, params: dict) -> str | None:
    """
    Функция запроса к API по методу GET.
    :params url: str - url запроса к API
    :params params: dict - параметры запроса

    :return response.text: str - текст запроса
    """

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

    except requests.exceptions.ReadTimeout:
        return ''


def post_request(url: str, params: dict) -> str | None:
    """
    Функция запроса к API по методу POST.
    :params url: str - url запроса к API
    :params params: dict - параметры запроса

    :return response.text: str - текст запроса
    """
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

    except requests.exceptions.ReadTimeout:
        return ''
