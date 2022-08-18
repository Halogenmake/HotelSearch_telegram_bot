from telebot import TeleBot
from config_data.config import BOT_TOKEN
from telebot.types import BotCommand
from interface.messages import DEFAULT_COMMANDS

lang = 'Ru'

bot = TeleBot(token=BOT_TOKEN)
bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS[lang].items()])

