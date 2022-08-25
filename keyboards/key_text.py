"""
Пакет содержит тексты inline кнопок на двух языках (где это требуется), а также callback inline кнопок. Каждая двуязычная переменная - словарь
с ключами Ru и En соответственно
"""


ENGLISH_KEY = 'English'
RUSSIAN_KEY = 'Русский'
EN_CALL = 'En'
RU_CALL = 'Ru'

LOWPRICE_KEY = {
    'Ru': 'Дешевые',
    'En': 'Lowprice'
}

HIGHPRICE_KEY = {
    'Ru': 'Дорогие',
    'En': 'Highprice'
}

BESTDEAL_KEY = {
    'Ru': 'Лучшие',
    'En': 'Bestdeal'
}

HISTORY_KEY = {
    'Ru': 'История',
    'En': 'History'
}

SET_LANG_KEY = {
    'Ru': 'Язык',
    'En': 'Language'
}

LOWPRICE_CALL = 'lowprice'
HIGHPRICE_CALL = 'highprice'
BESTDEAL_CALL = 'bestdeal'
HISTORY_CALL = 'history'
SET_LANG_CALL = 'set_lang'

CURRENCY_KEY_CALL = ('RUB', 'USD', 'EUR')

COUNT_HOTEL_CALL = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                    'eight': 8, 'nine': 9, 'ten': 10}

SELECT_PHOTO_KEY_CALL = {
    'Ru': {'yes': 'Да', 'no': 'Нет'},
    'En': {'yes': 'Yes', 'no': 'No'},
}

COUNT_PHOTO_CALL = {'uno': 1, 'dois': 2, 'tres': 3, 'quatro': 4, 'cinco': 5, 'seis': 6, 'sete': 7,
                    'oito': 8, 'nove': 9, 'dez': 10}