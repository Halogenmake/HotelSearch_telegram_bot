"""
Пакет содержит все сообщения бота на двух языках (где это требуется). Каждая двуязычная переменная - словарь
с ключами Ru и En соответственно
"""

from keyboards.key_text import *


DEFAULT_COMMANDS = {
    'Ru': {
        'start': "Запустить бота",
        'help': "Вывести справку",
        LOWPRICE_CALL: "Самые дешёвые отели в городе",
        HIGHPRICE_CALL: "Самые дорогие отели в городе",
        BESTDEAL_CALL: "Лучшие предложения",
        HISTORY_CALL: "История поиска отелей",
        SET_LANG_CALL: "Сменить язык интерфейса"
    },
    'En': {
        'start': "Bot start",
        'help': "Get the help",
        LOWPRICE_CALL: "The cheapest hotels in the city",
        HIGHPRICE_CALL: "The most expensive hotels in the city",
        BESTDEAL_CALL: "The best offers",
        HISTORY_CALL: "Hotel search history",
        SET_LANG_CALL: "Change the interface language"
    }
}

DEFAULT_COMMANDS_MENU = {
    'start': "Запустить бота / Bot start"
}

SELECT_LANG = 'Выберите язык интерфейа\n' \
              'Select interface laguage'

CHOICE_LANG = {
    'Ru': 'Выбран Русский язык',
    'En': 'English is selected'
}

LOWPRICE_STAE = {
    'Ru': 'Подбираем самые дешевые отели',
    'En': 'Select the cheapest hotels'
}

HIGHPRICE_STATE = {
    'Ru': 'Подбираем самые дорогие отели',
    'En': 'Select the most expensive hotels'
}

REQUEST_CARD_TEMPLATE = {
    'Ru':
        '<b>{}</b>\n'
        '<b>Город:</b> {}\n'
        '<b>Валюта:</b> {}\n'
        '<b>Дата заезда:</b> {}\n'
        '<b>Дата отъезда:</b> {}\n'
        '<b>Количество отелей:</b> {}\n'
        '<b>Количество фотографий отеля:</b> {}\n',
    'En':
        '<b>{}</b>\n'
        '<b>City:</b> {}\n'
        '<b>Currency:</b> {}\n'
        '<b>Check_in:</b> {}\n'
        '<b>Check_out:</b> {}\n'
        '<b>Number of hotels:</b> {}\n'
        '<b>Number of photos of the hotel:</b> {}\n'
}

SELECT_CITY = {
    'Ru': 'Введите город поиска отеля:',
    'En': 'Enter the city of the hotel search'
}

INCORRECT_CITY = {
    'Ru': 'Город не найден, введите город еще раз:',
    'En': 'The city was not found, enter the city again:'
}

CORRECT_CITY = {
    'Ru': 'Уточните город для поиска:',
    'En': 'Specify the city to search for:'
}

ERROR_CITY = {
    'Ru': 'Ошибка запроса, попробуйте ввести город снова:',
    'En': 'Request error, try entering the city again:'
}

CHOICE_CITY = {
    'Ru': 'Выбран город {}',
    'En': 'The city of {} is selected'
}

SELECT_CURRENCY = {
    'Ru': 'Выберите валюту:',
    'En': 'Choose a currency:'
}

CHOICE_CURRENCY = {
    'Ru': 'Выбрана валюта {}',
    'En': '{} currency is selected'
}

SELECT_COUNT_HOTEL = {
    'Ru': 'Выберите количество отображаемых отелей',
    'En': 'Select the number of hotels displayed'
}

CHOICE_COUNT_HOTEL = {
    'Ru': 'Будет показано {} отеля(ей)',
    'En': 'It will be shown {} hotels'
}

SELECT_CHECK_IN = {
    'Ru': 'Выберите дату заезда (формат 2022-08-22):',
    'En': 'Select the arrival date (format 2022-08-22):'
}

INCORRECT_CHECK_IN_FORMAT = {
    'Ru': 'Формат даты некорректен!\nВыберите дату заезда (формат 2022-08-22):',
    'En': 'The date format is incorrect!\nSelect the arrival date (format 2022-08-22):'
}

INCORRECT_CHECK_IN_DATA = {
    'Ru': 'Вы ввели прошедшую дату!\nВыберите дату заезда (формат 2022-08-22):',
    'En': 'You have entered a past date!!\nSelect the arrival date (format 2022-08-22):'
}

SELECT_CHECK_OUT = {
    'Ru': 'Выберите дату отъезда (формат 2022-08-22):',
    'En': 'Choose your departure date (format 2022-08-22):'
}

INCORRECT_CHECK_OUT_FORMAT = {
    'Ru': 'Формат даты некорректен!\nВыберите дату отъезда (формат 2022-08-22):',
    'En': 'The date format is incorrect!\nSelect the departure date (format 2022-08-22):'
}

INCORRECT_CHECK_OUT_DATA = {
    'Ru': 'Дата отъезда раньше даты заезда!\nВыберите дату заезда (формат 2022-08-22):',
    'En': 'The departure date is earlier than the arrival date!\nSelect the departure date (format 2022-08-22):'
}

SELECT_LOAD_PHOTO = {
    'Ru': 'Загрузить фото отелей?',
    'En': 'Upload photos of hotels?'
}

SELECT_COUNT_PHOTO = {
    'Ru': 'Выберите количество фотографий',
    'En': 'Select the number of photo'
}

CHOICE_COUNT_PHOTO = {
    'Ru': 'Будет показано {} фотографии(й)',
    'En': 'It will be shown {} photo'
}

PLEASE_WHAIT = {
    'Ru': 'Ищем подходящие варианты, пожалуйста, подождите...',
    'En': 'We are looking for suitable options, please wait...'
}

ERROR_HOTEL = {
    'Ru': 'В запросе произошла ошибка, попробуйте снова.',
    'En': 'An error occurred in the request, please try again.'
}

NOT_FOUND = {
    'Ru': 'К сожалению ничего не найдено\nПопробуйте изменить параметры поиска',
    'En': 'Unfortunately nothing was found\nTry changing the search parameters.'
}

SEARCH_COMPLETE = {
    'Ru': 'Поиск завершен.',
    'En': 'Search completed.'
}

HOTEL_TEMPLATE = {
    'Ru':
        '<b>Название отеля:</b> {}\n'
        '<b>Адрес отеля:</b> {}\n'
        '<b>Расстояние от центра:</b> {}\n'
        '<b>Цена за день:</b> {}\n'
        '<b>Рейтинг:</b> {}\n'
        '<b>Ссылка на отель:</b> {}\n',
    'En':
        '<b>Name of the hotel:</b> {}\n'
        '<b>Hotel address:</b> {}\n'
        '<b>Distance from the center:</b> {}\n'
        '<b>Price per day:</b> {}\n'
        '<b>Rating:</b> {}\n'
        '<b>Link:</b> {}\n'
}
