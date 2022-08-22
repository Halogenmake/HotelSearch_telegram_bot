from telebot import TeleBot, custom_filters
from telebot.types import BotCommand
from telebot.storage import StateMemoryStorage

from config_data.config import BOT_TOKEN
from interface.messages import DEFAULT_COMMANDS_MENU
from database.structure import DataBase

DataBase.user_table_create()

state_storage = StateMemoryStorage()
bot = TeleBot(token=BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS_MENU.items()])