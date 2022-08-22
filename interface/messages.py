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

REQUEST_CARD = {
    'Ru': 'Город: {}',

    'En': 'City: {}'
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