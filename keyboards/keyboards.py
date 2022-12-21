"""
Формирование всех необходимых клавиатур бота
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.key_text import *
from loader import logger

select_lang_key = InlineKeyboardMarkup()
select_lang_key.add(InlineKeyboardButton(text=ENGLISH_KEY, callback_data=EN_CALL),
                    InlineKeyboardButton(text=RUSSIAN_KEY, callback_data=RU_CALL))


@logger.catch
def main_menu_keys(lang: str) -> InlineKeyboardMarkup:
    """
    Функция формирования главного меню бота
    :param lang: str - язык интерфейса
    :return keyboard: InlineKeyboardMarkup - возвращает собранную клавиатуру
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=LOWPRICE_KEY[lang], callback_data=LOWPRICE_CALL),
                 InlineKeyboardButton(text=HIGHPRICE_KEY[lang], callback_data=HIGHPRICE_CALL),
                 InlineKeyboardButton(text=BESTDEAL_KEY[lang], callback_data=BESTDEAL_CALL))
    keyboard.add(InlineKeyboardButton(text=HISTORY_KEY[lang], callback_data=HISTORY_CALL),
                 InlineKeyboardButton(text=SET_LANG_KEY[lang], callback_data=SET_LANG_CALL))
    return keyboard


@logger.catch
def city_corr_keys(keylist: list[tuple]) -> InlineKeyboardMarkup:
    """
    Функция формирования кнопок уточнения города
    :param keylist: list[tuple] - список, содержащий названия городов и данные callback
    :return keyboard: InlineKeyboardMarkup - возвращает собранную клавиатуру
    """
    keyboard = InlineKeyboardMarkup()
    for keys in keylist:
        keyboard.add(InlineKeyboardButton(text=keys[0], callback_data=keys[1]))
    return keyboard


# def currency_keys() -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardMarkup()
#     keys = [InlineKeyboardButton(text=cur, callback_data=cur) for cur in CURRENCY_KEY_CALL]
#     keyboard.add(*keys)
#     return keyboard


@logger.catch
def hotels_count_keys(key: dict) -> InlineKeyboardMarkup:
    """
    Функция формирования кнопок для указания количества отображаемых отелей или количества загружаемых фото отеля
    :param key: dict - список, содержащий имена кнопок и данные callback
    :return keyboard: InlineKeyboardMarkup - возвращает собранную клавиатуру
    """
    keyboard = InlineKeyboardMarkup(row_width=5)
    keys = [InlineKeyboardButton(text=text, callback_data=call) for call, text in key.items()]
    keyboard.add(*keys)
    return keyboard


@logger.catch
def select_photo_keys(lang: str) -> InlineKeyboardMarkup:
    """
    Функция формирования кнопок для указания необходимости загрузки фотографий отеля
    :param lang: str - язык интерфейса
    :return keyboard: InlineKeyboardMarkup - возвращает собранную клавиатуру
    """
    keyboard = InlineKeyboardMarkup(row_width=5)
    keys = [InlineKeyboardButton(text=text, callback_data=call) for call, text in SELECT_PHOTO_KEY_CALL[lang].items()]
    keyboard.add(*keys)
    return keyboard


@logger.catch
def show_history_keys(lang: str) -> InlineKeyboardMarkup:
    """
    Функция формирования кнопок для работы с историей запросов
    :param lang: str - язык интерфейса
    :return keyboard: InlineKeyboardMarkup - возвращает собранную клавиатуру
    """
    keyboard = InlineKeyboardMarkup()
    keys = [InlineKeyboardButton(text=text, callback_data=call) for call, text in SELECT_HISTORY_KEY_CALL[lang].items()]
    keyboard.add(*keys)
    return keyboard
