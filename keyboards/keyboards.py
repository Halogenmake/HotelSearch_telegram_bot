from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.key_text import *

select_lang_key = InlineKeyboardMarkup()
select_lang_key.add(InlineKeyboardButton(text=ENGLISH_KEY, callback_data=EN_CALL),
                    InlineKeyboardButton(text=RUSSIAN_KEY, callback_data=RU_CALL))


def main_menu_key(lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=LOWPRICE_KEY[lang], callback_data=LOWPRICE_CALL),
                 InlineKeyboardButton(text=HIGHPRICE_KEY[lang], callback_data=HIGHPRICE_CALL),
                 InlineKeyboardButton(text=BESTDEAL_KEY[lang], callback_data=BESTDEAL_CALL))
    keyboard.add(InlineKeyboardButton(text=HISTORY_KEY[lang], callback_data=HIGHPRICE_CALL),
                 InlineKeyboardButton(text=SET_LANG_KEY[lang], callback_data=SET_LANG_CALL))
    return keyboard
