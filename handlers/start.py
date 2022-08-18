from telebot.types import Message, BotCommand
from loader import bot
from interface.messages import SELECT_LANG
from keyboards.keyboards import select_lang
from database.structure import DataBase, user
from interface.messages import DEFAULT_COMMANDS


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    if not DataBase.user_set(message.from_user.id):
        bot.send_message(message.from_user.id, SELECT_LANG, reply_markup=select_lang)
    else:
        bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS[user.get_lang()].items()])
        bot_help(message)


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[user.get_lang()].items()]
    bot.reply_to(message, '\n'.join(text))