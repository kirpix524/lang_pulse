import sqlite3
from sqlite3 import Connection
from datetime import datetime

from factories.user_word_factory import UserWordFactory
from models.user_dictionary import UserDictionary
from models.user_word import IBasicUserWord
from models.language import Language
from models.user import User
from repositories.word_repo import WordRepository
from storage.interfaces import IUserDictionaryStorage

class UserDictionarySQLiteStorage(IUserDictionaryStorage):
    def __init__(self, sql_data: dict[str, str]) -> None:
        self._conn: Connection = sqlite3.connect(sql_data['db_path'])
        self._conn.row_factory = sqlite3.Row
        self._sql_data = sql_data

    def __get_table_name(self, user: User, language: Language) -> str:
        name = f"{self._sql_data['user_dictionary_table_prefix']}_{user.username}_{language.lang_code}".lower()
        return name

    def __ensure_table(self, user: User, language: Language) -> None:
        table = self.__get_table_name(user, language)
        create_sql = (
            f"CREATE TABLE IF NOT EXISTS {table} ("
            "term TEXT NOT NULL, "
            "translation TEXT NOT NULL, "
            "added_at TEXT NOT NULL"
            ")"
        )
        self._conn.execute(create_sql)
        self._conn.commit()

    def load_dictionary(
        self,
        user: User,
        language: Language,
        word_repo: WordRepository
    ) -> UserDictionary:
        dictionary = UserDictionary(user, language, word_repo)
        self.__ensure_table(user, language)
        table = self.__get_table_name(user, language)
        cursor = self._conn.execute(
            f"SELECT term, translation, added_at FROM {table}"
        )
        words: list[IBasicUserWord] = []
        for row in cursor.fetchall():
            term: str = row['term']
            translation: str = row['translation']
            added_at_str: str = row['added_at']
            added_at: datetime = (
                datetime.fromisoformat(added_at_str)
                if added_at_str
                else datetime.now()
            )
            word = word_repo.find_word(term, translation)
            user_word = UserWordFactory.create_word(language, word, added_at)
            words.append(user_word)
        dictionary.set_words(words)
        return dictionary

    def save_dictionary(self, dictionary: UserDictionary) -> None:
        user: User = dictionary.get_user()
        language: Language = dictionary.get_language()
        self.__ensure_table(user, language)
        table = self.__get_table_name(user, language)
        # Clear existing entries
        self._conn.execute(f"DELETE FROM {table}")
        # Insert current words
        for word in dictionary.get_words():
            params = (
                word.word.term,
                word.word.translation,
                word.get_added_at().isoformat()
            )
            self._conn.execute(
                f"INSERT INTO {table} (term, translation, added_at) VALUES (?, ?, ?)",
                params
            )
        self._conn.commit()