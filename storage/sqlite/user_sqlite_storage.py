import sqlite3
from typing import List

from models.user import User
from storage.interfaces import IUserStorage


class UserSQLiteStorage(IUserStorage):
    def __init__(self, sql_data: dict[str, str]) -> None:
        self._sql_data = sql_data
        self.__connection: sqlite3.Connection = sqlite3.connect(sql_data["db_path"])
        self.__initialize_table()

    def __initialize_table(self) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._sql_data["users_table_name"]} (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL
            )
            """
        )
        self.__connection.commit()

    def load_user_list(self) -> List[User]:
        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT id, username FROM {self._sql_data["users_table_name"]}")
        rows = cursor.fetchall()
        return [User(username=row[1], userid=row[0]) for row in rows]

    def save_user_list(self, user_list: List[User]) -> None:
        cursor = self.__connection.cursor()
        for user in user_list:
            cursor.execute(
                f"""
                    INSERT INTO {self._sql_data["users_table_name"]} (id, username)
                        VALUES (?, ?)
                        ON CONFLICT(id) DO UPDATE SET username = excluded.username
                    """,
                (user.userid, user.username)
            )
        self.__connection.commit()

    def save_user(self, user: User) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            f"""
                INSERT INTO {self._sql_data["users_table_name"]} (id, username)
                    VALUES (?, ?)
                    ON CONFLICT(id) DO UPDATE SET username = excluded.username
                """,
            (user.userid, user.username)
        )
        self.__connection.commit()

    def __del__(self) -> None:
        if hasattr(self, '_UserSQLiteStorage__connection'):
            self.__connection.close()
