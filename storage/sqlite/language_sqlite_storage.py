import sqlite3

from models.language import Language
from storage.interfaces import ILanguageStorage


class LanguageSqliteStorage(ILanguageStorage):
    def __init__(self, sql_data: dict[str, str]) -> None:
        self._sql_data = sql_data
        self.__connection: sqlite3.Connection = sqlite3.connect(sql_data["db_path"])
        self.__init_table()

    def __init_table(self) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._sql_data["languages_table_name"]} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT NOT NULL
            )
            """
        )
        self.__connection.commit()

    def save_language_list(self, language_list: list[Language]) -> None:
        cursor = self.__connection.cursor()
        for language in language_list:
            cursor.execute(f"INSERT INTO {self._sql_data['languages_table_name']} (id, name, code) VALUES (?, ?, ?)", (language.lang_id, language.lang_name, language.lang_code))
        self.__connection.commit()

    def save_language(self, language: Language) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(f"INSERT INTO {self._sql_data['languages_table_name']} "
                       f"(id, name, code) VALUES (?, ?, ?)"
                       "ON CONFLICT(id) DO UPDATE SET name = excluded.lang_name, code = excluded.lang_code",
                       (language.lang_id, language.lang_name, language.lang_code))
        self.__connection.commit()

    def load_language_list(self) -> list[Language]:
        cursor = self.__connection.cursor()
        cursor.execute(f"SELECT id, name, code FROM {self._sql_data['languages_table_name']}")
        rows = cursor.fetchall()
        return [Language(lang_id=row[0], lang_name=row[1], lang_code=row[2]) for row in rows]

    def __del__(self) -> None:
        if hasattr(self, '_LanguageSqliteStorage__connection'):
            self.__connection.close()