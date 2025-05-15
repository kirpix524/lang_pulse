import sqlite3
from sqlite3 import Connection

from factories.word_factory import WordFactory
from models.language import Language
from models.word import IBasicWord
from factories.word_repo_table_schema_factory import WordRepoTableSchemaFactory
from storage.interfaces import IWordStorage
from app.config import WORD_REPO_SQL_DATA


class WordSQLiteStorage(IWordStorage):
    def __init__(self, db_path: str) -> None:
        self._conn: Connection = sqlite3.connect(db_path)

    def load_word_list(self, language: Language) -> list[IBasicWord]:
        schema = WordRepoTableSchemaFactory.create_schema(language, WORD_REPO_SQL_DATA["table_prefix"])
        schema.create_table(self._conn)
        cursor = self._conn.execute(schema.select_all_words())
        return [
            WordFactory.from_line(language, schema.row_to_line(row))
            for row in cursor.fetchall()
        ]

    def save_word(self, word: IBasicWord, language: Language) -> None:
        schema = WordRepoTableSchemaFactory.create_schema(language, WORD_REPO_SQL_DATA["table_prefix"])
        schema.create_table(self._conn)
        params = schema.get_insert_params(word)
        self._conn.execute(schema.insert_word(), params)
        self._conn.commit()

    def save_word_list(self, words: list[IBasicWord], language: Language) -> None:
        schema = WordRepoTableSchemaFactory.create_schema(language, WORD_REPO_SQL_DATA["table_prefix"])
        schema.create_table(self._conn)
        for w in words:
            self._conn.execute(schema.insert_word(), schema.get_insert_params(w))
        self._conn.commit()
