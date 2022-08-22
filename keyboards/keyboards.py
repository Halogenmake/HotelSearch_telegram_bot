from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.key_text import *

select_lang_key = InlineKeyboardMarkup()
select_lang_key.add(InlineKeyboardButton(text=ENGLISH_KEY, callback_data=EN_CALL),
                    InlineKeyboardButton(text=RUSSIAN_KEY, callback_data=RU_CALL))


def main_menu_keys(lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=LOWPRICE_KEY[lang], callback_data=LOWPRICE_CALL),
                 InlineKeyboardButton(text=HIGHPRICE_KEY[lang], callback_data=HIGHPRICE_CALL),
                 InlineKeyboardButton(text=BESTDEAL_KEY[lang], callback_data=BESTDEAL_CALL))
    keyboard.add(InlineKeyboardButton(text=HISTORY_KEY[lang], callback_data=HIGHPRICE_CALL),
                 InlineKeyboardButton(text=SET_LANG_KEY[lang], callback_data=SET_LANG_CALL))
    return keyboard


def city_corr_keys(keylist: list[tuple]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for keys in keylist:
        keyboard.add(InlineKeyboardButton(text=keys[1], callback_data=keys[0]))
    return keyboard


def currency_keys() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keys = [InlineKeyboardButton(text=cur, callback_data=cur) for cur in CURRENCY_KEY_CALL]
    keyboard.add(*keys)
    return keyboard


def hotels_count_keys(keys: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    keys = [InlineKeyboardButton(text=text, callback_data=call) for call, text in keys.items()]
    keyboard.add(*keys)
    return keyboard

def select_photo_keys(lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    keys = [InlineKeyboardButton(text=text, callback_data=call) for call, text in SELECT_PHOTO_KEY_CALL[lang].items()]
    keyboard.add(*keys)
    return keyboard