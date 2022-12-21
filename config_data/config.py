"""
Пакет содержит базовые настройки бота
"""


import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

HEADERS_GET = {
    'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
    'X-RapidAPI-Key': RAPID_API_KEY
}

HEADERS_POST = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}



#Выдача списка городов
SEARCH_CITY_ENDSWITH = 'locations/v3/search'

#Выдача списков отелей
HOTEL_LIST_ENDSWITH = 'properties/v2/list'

#Выдача списка фотографий
PHOTO_ENDSWITH = 'properties/v2/detail'

URL_HOTEL = 'https://www.hotels.com/h{}.Hotel-Information'

#Параметры запроса списка городов
CITY_SEARCH = {
        'q': '',
        'locale': ''
    }

#Параметры запроса списка отелей
PAYLOAD_HOTEL_LIST = {
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

#Параметры запроса информации об отеле
PAYLOAD_HOTEL_INFORMATION = {
         "currency": "USD",
         "eapid": 1,
         "locale": "en_US",
         "siteId": 300000001,
         "propertyId": ''
     }