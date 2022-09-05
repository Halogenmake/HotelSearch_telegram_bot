"""
Пакет, содержащий необходимые функции запросов по API и т.д.
"""


import requests
import string
from requests import Response
from config_data.config import URL_SEARCH, HEADERS, URL_PROPERTY_LIST, URL_PHOTO
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
        'query': '',
        'locale': ''
    }

    for sym in text:
        if sym not in string.printable:
            CITY_SEARCH['locale'] = 'ru_RU'
            break
    else:
        CITY_SEARCH['locale'] = 'en_US'

    Users_State.state_record(user_id=user_id, key='locate', value=CITY_SEARCH['locale'])
    CITY_SEARCH['query'] = text
    response = requests.request('GET', URL_SEARCH, headers=HEADERS, params=CITY_SEARCH, timeout=15)
    return response


def request_hotel_search(user_id: int, command: str) -> Response:
    """
    Запрос к API на отель по параметрам, указанным в HOTEL_PROPERTY_LIST.
    Недостающие данные для запроса берутся из текущего стейта пользователя Users_State.state_get.
    В этом же запросе определяется, в каком порядке будут упорядочены результаты, что определяет результаты
    для LOWPRICE и HIGHPRICE
    :param user_id: nt id пользователя в телеграме
    :return: Response
    """
    HOTEL_PROPERTY_LIST_BEST = {
        'destinationId': '',
        'pageNumber': '1',
        'pageSize': '25',
        'checkIn': '',
        'checkOut': '',
        'adults1': '1',
        'priceMin': '',
        'priceMax': '',
        'sortOrder': 'DISTANCE_FROM_LANDMARK',
        'locale': '',
        'currency': ''
    }

    HOTEL_PROPERTY_LIST = {
        'destinationId': '',
        'pageNumber': '1',
        'pageSize': '25',
        'checkIn': '',
        'checkOut': '',
        'adults1': '1',
        'sortOrder': '-PRICE',
        'locale': '',
        'currency': ''
    }

    if command != BESTDEAL_CALL:
        user_info = Users_State.state_get(user_id=user_id,
                                          key=('city_id', 'check_in', 'check_out', 'curr', 'locate'))

        if command == LOWPRICE_CALL:
            HOTEL_PROPERTY_LIST['sortOrder'] = 'PRICE'
        HOTEL_PROPERTY_LIST['destinationId'], HOTEL_PROPERTY_LIST['checkIn'], HOTEL_PROPERTY_LIST['checkOut'], \
        HOTEL_PROPERTY_LIST['currency'], HOTEL_PROPERTY_LIST['locale'] = user_info
        response = requests.request('GET', URL_PROPERTY_LIST, headers=HEADERS, params=HOTEL_PROPERTY_LIST, timeout=15)

    else:
        user_info = Users_State.state_get(user_id=user_id,
                                          key=('city_id', 'check_in', 'check_out', 'low_price', 'high_price', 'curr', 'locate'))

        HOTEL_PROPERTY_LIST_BEST['destinationId'], HOTEL_PROPERTY_LIST_BEST['checkIn'], HOTEL_PROPERTY_LIST_BEST['checkOut'], \
        HOTEL_PROPERTY_LIST_BEST['priceMin'], HOTEL_PROPERTY_LIST_BEST['priceMax'], \
        HOTEL_PROPERTY_LIST_BEST['currency'], HOTEL_PROPERTY_LIST_BEST['locale'] = user_info
        response = requests.request('GET', URL_PROPERTY_LIST, headers=HEADERS, params=HOTEL_PROPERTY_LIST_BEST, timeout=15)
    return response


def request_get_photo(hotel_id: int) -> Response:
    """
    Запрос к API на получение фото отеля по шаблону REQUEST_PHOTO = {'id': hotel_id}
    :param hotel_id: id-отеля, полученного при запросе request_hotel_search
    :return: Response
    """

    REQUEST_PHOTO = {'id': hotel_id}
    response = requests.request('GET', URL_PHOTO, headers=HEADERS, params=REQUEST_PHOTO, timeout=15)
    return response
