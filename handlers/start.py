from telebot.types import Message, CallbackQuery
from loader import bot
from interface.messages import SELECT_LANG
from keyboards.keyboards import select_lang_key, main_menu_key
from database.structure import DataBase  # , user
from interface.messages import DEFAULT_COMMANDS, CHOICE_LANG
from keyboards.key_text import EN_CALL, RU_CALL, SET_LANG_CALL


def lang_func(lang: str, user_id: int) -> None:
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[lang].items()]
    bot.send_message(user_id, '\n'.join(text), reply_markup=main_menu_key(lang))


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    if not DataBase.user_set(message.from_user.id):
        bot.send_message(message.from_user.id, SELECT_LANG, reply_markup=select_lang_key)
    else:
        bot_help(message)


@bot.message_handler(commands=[SET_LANG_CALL])
def select_lang_reply(message: Message) -> None:
    bot.send_message(message.from_user.id, SELECT_LANG, reply_markup=select_lang_key)


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    lang = DataBase.user_get_lang(user_id=message.from_user.id)
    lang_func(lang=lang, user_id=message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data in [EN_CALL, RU_CALL, SET_LANG_CALL])
def select_lang(call: CallbackQuery) -> None:
    if call.data == SET_LANG_CALL:
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=SELECT_LANG, reply_markup=select_lang_key
        )
    else:
        DataBase.user_set_lang(lang=call.data, user_id=call.from_user.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=CHOICE_LANG[call.data]
        )
        lang_func(lang=call.data, user_id=call.from_user.id)
