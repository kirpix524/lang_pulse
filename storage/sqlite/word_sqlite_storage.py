import sqlite3
from sqlite3 import Connection
from typing import Dict

from factories.word_factory import WordFactory
from models.language import Language
from models.word import IBasicWord
from factories.word_repo_table_schema_factory import WordRepoTableSchemaFactory
from storage.interfaces import IWordStorage
from app.config import WORD_REPO_SQL_DATA
from storage.sqlite.schema.word_repo_schema import IWordRepoTableSchema


class WordSQLiteStorage(IWordStorage):
    def __init__(self, db_path: str) -> None:
        self._conn: Connection = sqlite3.connect(db_path)
        self._schema_cache: Dict[str, IWordRepoTableSchema] = {}

    def _get_schema(self, language: Language) -> IWordRepoTableSchema:
        code = language.lang_code.lower()
        if code not in self._schema_cache:
            schema = WordRepoTableSchemaFactory.create_schema(
                language, WORD_REPO_SQL_DATA["table_prefix"]
            )
            schema.create_table(self._conn)
            self._schema_cache[code] = schema
        return self._schema_cache[code]

    def load_word_list(self, language: Language) -> list[IBasicWord]:
        schema = self._get_schema(language)
        cursor = self._conn.execute(schema.select_all_words())
        return [
            WordFactory.from_line(language, schema.row_to_line(row))
            for row in cursor.fetchall()
        ]

    def save_word(self, word: IBasicWord, language: Language) -> None:
        schema = self._get_schema(language)
        params = schema.get_insert_params(word)
        self._conn.execute(schema.insert_word(), params)
        self._conn.commit()

    def save_word_list(self, words: list[IBasicWord], language: Language) -> None:
        schema = self._get_schema(language)
        for w in words:
            self._conn.execute(schema.insert_word(), schema.get_insert_params(w))
        self._conn.commit()
