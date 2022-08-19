from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


select_lang_key = InlineKeyboardMarkup()
select_lang_key.add(InlineKeyboardButton(text='English', callback_data='En'),
                InlineKeyboardButton(text='Русский', callback_data='Ru'))