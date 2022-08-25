from dataclasses import dataclass
import sqlite3
from typing import Any, Union

from telebot.handler_backends import StatesGroup, State
from loader import bot


@dataclass
class Data_request_state(StatesGroup):
    city: str = State()
    check_in: str = State()
    check_out: str = State()


class Users_State:

    @classmethod
    def state_record(cls, user_id: int, key: Union[tuple, Any], value: Union[tuple, Any]) -> None:
        with bot.retrieve_data(user_id=user_id) as data:
            if not isinstance(key, tuple) or not isinstance(value, tuple):
                data[key] = value
            else:
                for i_key, i_value in zip(key, value):
                    data[i_key] = i_value

    @classmethod
    def state_get(cls, user_id: int, key: Union[tuple, Any]) -> Any:
        with bot.retrieve_data(user_id=user_id) as data:
            if not isinstance(key, tuple):
                return data[key]
            else:
                return tuple(data[i_key] for i_key in key)

    @classmethod
    def state_print(cls, user_id: int):
        with bot.retrieve_data(user_id=user_id) as data:
            print()
            for i_data in data.items():
                print(i_data)



class DataBase:

    @classmethod
    def user_table_create(cls) -> None:
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT name FROM 'sqlite_master' "
                "WHERE type='table' AND name='users';"
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.executescript(
                    "CREATE TABLE 'users' ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "user_id INTEGER NOT NULL, "
                    "lang TEXT NOT NULL)"
                )

    @classmethod
    def user_set(cls, user_id: int) -> bool:
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT * FROM 'users' WHERE user_id = ?", (user_id,)
            )
            exist = cursor.fetchone()
            if not exist:
                cursor.execute(
                    "INSERT INTO 'users' ("
                    "user_id, lang) "
                    "VALUES (?, ?)", (user_id, 'Ru')
                )
                return False
            else:
                return True

    @classmethod
    def user_set_lang(cls, lang: str, user_id: int) -> None:
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "UPDATE users SET lang = ?"
                "WHERE user_id = ?", (lang, user_id,)
            )

    @classmethod
    def user_get_lang(cls, user_id: int) -> str:
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT lang FROM 'users' "
                "WHERE user_id = ?;", (user_id,)
            )
            return cursor.fetchone()[0]
