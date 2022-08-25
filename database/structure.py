"""
Пакет содержит классы для работы с объектами бота:

Data_request_state(StatesGroup) - датакласс для создания стейтов бота
Users_State - датакласс для получения и записи данных в стейт
DataBase - датакласс для работы с базой данных

"""

from dataclasses import dataclass
import sqlite3
from typing import Any, Union

from telebot.handler_backends import StatesGroup, State
from loader import bot


@dataclass
class Data_request_state(StatesGroup):
    """
    Датакласс для создания стейтов бота
    """
    city: str = State()
    check_in: str = State()
    check_out: str = State()


class Users_State:
    """
    Датакласс для получения и записи данных в стейт
    """

    @classmethod
    def state_record(cls, user_id: int, key: Union[tuple, Any], value: Union[tuple, Any]) -> None:
        """
        Классметод записи данных в стейт.
        Для зхаписи можно передавать как единичные значения, так и кортежи ключей и соответствующие им данные

        :param user_id: id прользователя в телеграме,
        :param key: ключи, по которым происходит запись,
        :param value: значения, которые должны быть записаны по переданным ключам
        """

        with bot.retrieve_data(user_id=user_id) as data:
            if not isinstance(key, tuple) or not isinstance(value, tuple):
                data[key] = value
            else:
                for i_key, i_value in zip(key, value):
                    data[i_key] = i_value

    @classmethod
    def state_get(cls, user_id: int, key: Union[tuple, str]) -> Any:
        """
        Классметод получения данных из стейта пользователя.
        Для получения можно передавать как единичные значения ключей, так и кортеж ключей

        :param user_id: int id прользователя в телеграме,
        :param key: [str, tuple] ключи, по которым происходит выдача данных,
        :return: [Any] единичное знаение или кортеж данных по переданным ключам
        """

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
    """
    Датакласс для работы с базой данных
    """
    @classmethod
    def user_table_create(cls) -> None:
        """
        Классметод, создающий таблицу пользователей users, если её нет.
        """
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
        """
        Классметод, создающий запись пользователя по user_id (id прользователя в телеграме)
        в таблице пользоватеей users, если этой записи нет
        :param user_id: int id прользователя в телеграме
        :return: bool
        """
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
        """
        Записывает в таблицу пользователя по user_id (id прользователя в телеграме)
        данные о языке интерфейса

        :param lang: str язык пользователя,
        :param user_id: int id прользователя в телеграме
        """

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
