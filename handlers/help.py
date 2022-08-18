from telebot.types import Message
from interface.messages import DEFAULT_COMMANDS
from loader import bot, lang


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS[lang].items()]
    bot.reply_to(message, '\n'.join(text))
