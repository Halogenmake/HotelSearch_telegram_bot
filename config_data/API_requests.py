import requests
import string
from requests import Response
from config_data.config import URL_SEARCH, HEADERS, URL_PROPERTY_LIST, URL_PHOTO
from database.structure import Users_State
from keyboards.key_text import LOWPRICE_CALL


def request_city_search(user_id: int, text: str) -> Response:
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


def request_hotel_search(user_id: int) -> Response:
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

    user_info = Users_State.state_get(user_id=user_id,
                                      key=('command', 'city_id', 'check_in', 'check_out', 'curr', 'locate'))

    if user_info[0] == LOWPRICE_CALL:
        HOTEL_PROPERTY_LIST['sortOrder'] = 'PRICE'
    HOTEL_PROPERTY_LIST['destinationId'], HOTEL_PROPERTY_LIST['checkIn'], HOTEL_PROPERTY_LIST['checkOut'], \
    HOTEL_PROPERTY_LIST['currency'], HOTEL_PROPERTY_LIST['locale'] = user_info[1:]
    response = requests.request('GET', URL_PROPERTY_LIST, headers=HEADERS, params=HOTEL_PROPERTY_LIST, timeout=15)
    return response


def request_get_photo(hotel_id: int) -> Response:
    REQUEST_PHOTO = {'id': hotel_id}
    response = requests.request('GET', URL_PHOTO, headers=HEADERS, params=REQUEST_PHOTO, timeout=15)
    return response
