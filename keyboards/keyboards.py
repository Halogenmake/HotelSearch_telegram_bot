from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

select_lang = InlineKeyboardMarkup()
select_lang.add(InlineKeyboardButton(text='English', callback_data='En'),
                InlineKeyboardButton(text='Русский', callback_data='Ru'))