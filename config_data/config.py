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

HEADERS = {
    'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
    'X-RapidAPI-Key': RAPID_API_KEY
}

HEADERS_POST = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


#Выдача списка городов
URL_SEARCH_CITY = 'https://hotels4.p.rapidapi.com/locations/v3/search'

#Выдача списков отелей
URL_HOTEL_LIST = 'https://hotels4.p.rapidapi.com/properties/v2/list'

#Выдача списка фотографий
URL_PHOTO = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

URL_HOTEL = 'https://www.hotels.com/h{}.Hotel-Information'

