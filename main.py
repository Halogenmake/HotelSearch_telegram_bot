from loader import bot
from database.structure import DataBase
import handlers

if __name__ == '__main__':
    DataBase.user_table_create()
    bot.infinity_polling()
