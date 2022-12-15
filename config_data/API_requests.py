"""
Пакет, содержащий необходимые функции запросов по API и т.д.
"""

import requests
import string
from requests import Response
from config_data.config import URL_SEARCH_CITY, HEADERS, HEADERS_POST, URL_HOTEL_LIST, URL_PHOTO
from database.structure import Users_State
from keyboards.key_text import LOWPRICE_CALL, BESTDEAL_CALL


def request_city_search(user_id: int, text: str) -> Response:
    """
    Запрос на уточнение города, где будет происходить поиск отелей
    :param user_id: int id пользователя в телеграме
    :param text: str текст запроса (содержит строку, введенную пользователем)
    :return: Response
    """
    CITY_SEARCH = {
        'q': '',
        'locale': ''
    }

    for sym in text:
        if sym not in string.printable:
            CITY_SEARCH['locale'] = 'ru_RU'
            break
    else:
        CITY_SEARCH['locale'] = 'en_US'

    Users_State.state_record(user_id=user_id, key='locate', value=CITY_SEARCH['locale'])
    CITY_SEARCH['q'] = text
    response = requests.request('GET', url=URL_SEARCH_CITY, headers=HEADERS, params=CITY_SEARCH, timeout=15)
    return response


def request_hotel_list(user_id: int, command: str) -> Response:
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": "3023"},
        "checkInDate": {
            "day": 12,
            "month": 12,
            "year": 2022
        },
        "checkOutDate": {
            "day": 13,
            "month": 12,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 1
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {
            "price": {
                "max": 15000000,
                "min": 1
            },
            "availableFilter": "SHOW_AVAILABLE_ONLY"
        }
    }

    if command != BESTDEAL_CALL:
        user_info = Users_State.state_get(user_id=user_id, key=('city_id', 'locate'))

        if command != LOWPRICE_CALL:
            payload['sort'] = 'PRICE_HIGH_TO_LOW'

        payload['destination']['regionId'], payload['locale'] = user_info

    else:
        user_info = Users_State.state_get(user_id=user_id, key=('city_id', 'locate', 'low_price', 'high_price'))

        payload['destination']['regionId'], payload['locale'], payload['filters']['price']['min'],\
        payload['filters']['price']['max'] = user_info

    payload['checkInDate']['year'], payload['checkInDate']['month'], \
    payload['checkInDate']['day'] = map(int, Users_State.state_get(user_id=user_id, key='check_in').split('-'))

    payload['checkOutDate']['year'], payload['checkOutDate']['month'], \
    payload['checkOutDate']['day'] = map(int, Users_State.state_get(user_id=user_id, key='check_out').split('-'))

    response = requests.request('POST', url=URL_HOTEL_LIST, json=payload, headers=HEADERS_POST, timeout=15)

    return response


def request_get_information(user_id: int, hotel_id: int) -> Response:
    """
    Запрос к API на получение фото отеля по шаблону REQUEST_PHOTO = {'id': hotel_id}
    :user_id: int: id пользователя в телеграме
    : hotel_id: int: id-отеля, полученного при запросе request_hotel_search
    :return: Response
    """

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    payload["locale"] = Users_State.state_get(user_id=user_id, key='locate')

    response = requests.request("POST", URL_PHOTO, json=payload, headers=HEADERS, timeout=15)
    return response
