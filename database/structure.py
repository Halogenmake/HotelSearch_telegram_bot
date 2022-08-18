from dataclasses import dataclass
import sqlite3


@dataclass
class User:
    user_id: int = 0
    user_lang: str = 'Ru'


class User_methods:
    def __init__(self) -> None:
        self.user: User = User()

    def get_lang(self) -> str:
        return self.user.user_lang

    def user_from_base(self, keys: tuple) -> None:
        _, self.user.user_id, self.user.user_lang = keys

    def user_to_base(self) -> tuple:
        return (
            self.user.user_id,
            self.user.user_lang
        )

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
    def user_set(cls, user_id) -> bool:
        with sqlite3.connect('database.db') as data:
            cursor = data.cursor()
            cursor.execute(
                "SELECT * FROM 'users' WHERE user_id = ?", (user_id, )
            )
            exist = cursor.fetchone()
            print(exist)
            if not exist:
                cursor.execute(
                    "INSERT INTO 'users' ("
                "user_id, lang) "
                "VALUES (?, ?)", (user_id, 'Ru')
                )
                return False
            else:
                user.user_from_base(exist)
                return True

user = User_methods()
