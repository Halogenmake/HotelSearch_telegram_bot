from loader import bot
import handlers
from database.structure import DataBase


if __name__ == '__main__':
    DataBase.user_table_create()
    bot.infinity_polling()
