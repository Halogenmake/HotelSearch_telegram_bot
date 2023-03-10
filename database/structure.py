"""
Пакет содержит классы для работы с объектами бота:

Data_request_state(StatesGroup) - дата-класс для создания стейтов бота
Users_State - дата-класс для получения и записи данных в стейт
DataBase - дата-класс для работы с базой данных

"""

from dataclasses import dataclass
import sqlite3
from typing import Any, Union
import datetime

from telebot.handler_backends import StatesGroup, State
from loader import bot


@dataclass
class Data_request_state(StatesGroup):
    """
    Дата-класс для создания стейтов бота
    """
    city: str = State()
    check_in: str = State()
    check_out: str = State()
    low_price: str = State()
    high_price: str = State()
    low_dist: str = State()
    high_dist: str = State()
    standby: str = State()


class Users_State:
    """
    Датакласс для получения и записи данных в стейт.
    Данные, записываемые в сетйт:
    'lang': str - язык интерфейса
    'command': str - введенная команда
    'city': str - Город поиска
    'city_id': str - идентификатор города
    'curr': str - валюта поиска
    'hotel_count': int - количество отелей
    'check_in': str - время заезда
    'check_out': str - время отъезда
    'photo': bool - наличие фото
    'photo_count' - количество фото
    'date' - дата и время выполнения запроса
    """

    @classmethod
    def state_record(cls, user_id: int, key: Union[tuple, Any], value: Union[tuple, Any]) -> None:
        """
        Класс-метод записи данных в стейт.
        Для записи можно передавать как единичные значения, так и кортежи ключей и соответствующие им данные

        :param user_id: id пользователя в телеграме,
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
        Класс-метод получения данных из стейта пользователя.
        Для получения можно передавать как единичные значения ключей, так и кортеж ключей

        :param user_id: int id пользователя в телеграме,
        :param key: [str, tuple] ключи, по которым происходит выдача данных,
        :return: [Any] единичное значение или кортеж данных по переданным ключам
        """

        with bot.retrieve_data(user_id=user_id) as data:
            if not isinstance(key, tuple):
                return data[key]
            else:
                return tuple(data[i_key] for i_key in key)


class DataBase:
    """
    Датакласс для работы с базой данных
    """

    @classmethod
    def user_table_create(cls) -> None:
        """
        Классметод, создающий таблицу пользователей users (если её нет)
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
    def request_table_create(cls) -> None:
        """
        Классметод, создающий таблицу запросов requests (если её нет)
        """
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT name FROM 'sqlite_master' "
                "WHERE type='table' AND name='requests';"
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.executescript(
                    "CREATE TABLE 'requests' ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "content TEXT NOT NULL,"
                    "user_id INTEGER NOT NULL,"
                    "date TEXT NOT NULL)"
                )

    @classmethod
    def hotels_table_create(cls) -> None:
        """
        Классметод, создающий таблицу отелей hotels (если её нет)
        """
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT name FROM 'sqlite_master' "
                "WHERE type='table' AND name='hotels';"
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.executescript(
                    "CREATE TABLE 'hotels' ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "content TEXT NOT NULL,"
                    "photo TEXT NOT NULL,"
                    "requests_id INTEGER NOT NULL,"
                    "FOREIGN KEY (requests_id) REFERENCES requests(id) ON DELETE CASCADE)"
                )

    @classmethod
    def user_set(cls, user_id: int) -> bool:
        """
        Классметод, создающий запись пользователя по user_id (id пользователя в телеграме)
        в таблице пользователей users, если этой записи нет
        :param user_id: int id пользователя в телеграме
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
        Записывает в таблицу пользователя по user_id (id пользователя в телеграме)
        данные о языке интерфейса

        :param lang: str язык пользователя,
        :param user_id: int id пользователя в телеграме
        """

        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "UPDATE users SET lang = ?"
                "WHERE user_id = ?", (lang, user_id,)
            )

    @classmethod
    def user_get_lang(cls, user_id: int) -> str:
        """
        Классметод, возвращающий язык интерфейса для пользователя по user_id (id пользователя в телеграме)
        :param user_id: int id пользователя в телеграме
        :return cursor.fetchone()[0]: str
        """

        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT lang FROM 'users' "
                "WHERE user_id = ?;", (user_id,)
            )
            return cursor.fetchone()[0]

    @classmethod
    def request_set(cls, user_id: int, content: str) -> None:
        """
        Классметод, записывающий по user_id (id пользователя в телеграме) карточку запроса в БД

        :param user_id: int id пользователя в телеграме
        :param content: str - карточка запроса
        """

        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "INSERT INTO 'requests' ("
                "content, user_id, date) "
                "VALUES (?, ?, ?)",
                (content, user_id, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
            )

    @classmethod
    def hotels_set(cls, user_id: int, content: str, photo: str) -> None:
        """
        Классметод, записывающий по user_id (id пользователя в телеграме) карточку найденного отеля

        :param user_id: int id пользователя в телеграме
        :param content: str - карточка запроса
        :param photo: str - список ссылк на фотографии отеля
        """
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT id FROM 'requests' "
                "WHERE user_id = ? ORDER BY id DESC", (user_id,)
            )
            requests_id, *_ = cursor.fetchone()
            cursor.execute(
                "INSERT INTO 'hotels' ("
                "content, photo, requests_id) "
                "VALUES (?, ?, ?)", (content, photo, requests_id)
            )

    @classmethod
    def history_requests_get(cls, user_id: int, limit: int) -> list[Any]:
        """
        Классметод, возвращающий из БД по user_id (id пользователя в телеграме) его запросы
        (или все, или в количестве limit). результат упорядочивается от ранней записи к более поздней

        :param user_id: int id пользователя в телеграме
        :param limit: int - количество выдаваемых записей запросов пользователя

        :return requests - список кортежей запроса, содержащий id (id запроса) и content (карточка запроса)
        """

        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT id, content, date FROM requests "
                "WHERE user_id = ? ORDER BY id DESC "
                "LIMIT ?;", (user_id, limit,)
            )
            requests = cursor.fetchall()
            return requests

    @classmethod
    def history_hotels_get(cls, request_id: int) -> list[Any]:
        """
        Классметод, возвращающий из БД по id запроса отели, которые были найдены

        :request_id: int - id запроса в БД

        :return requests - список кортежей запроса, содержащий content (карточка отеля), photo (список фотографий отеля)
        """
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT content, photo FROM hotels "
                "WHERE requests_id = ?;", (request_id,)
            )
            requests = cursor.fetchall()
            return requests
