from telebot.types import Message, CallbackQuery
from loader import bot
from interface.messages import SELECT_LANG
from keyboards.keyboards import select_lang_key
from database.structure import DataBase, user
from interface.messages import DEFAULT_COMMANDS, CHOICE_LANG


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    if not DataBase.user_set(message.from_user.id):
        bot.send_message(message.from_user.id, SELECT_LANG, reply_markup=select_lang_key)
    else:
        bot_help(message)


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[user.get_lang()].items()]
    bot.send_message(message.from_user.id, '\n'.join(text))

@bot.callback_query_handler(func=lambda call: call.data in ['En', 'Ru'])
def select_lang(call: CallbackQuery):
    DataBase.user_set_lang(lang=call.data, user_id=user.get_id())
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=CHOICE_LANG[call.data]
    )
