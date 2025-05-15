from abc import ABC, abstractmethod
from sqlite3 import Connection
from models.language import Language
from models.word import IBasicWord

class IWordRepoTableSchema(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass
    @abstractmethod
    def table_name(self) -> str: ...
    @abstractmethod
    def create_table(self, conn: Connection) -> None: ...
    @abstractmethod
    def select_all_words(self) -> str: ...
    @abstractmethod
    def select_word(self, word: IBasicWord) -> str: ...
    @abstractmethod
    def insert_word(self) -> str: ...
    @abstractmethod
    def get_insert_params(self, word: IBasicWord) -> tuple: ...
    @abstractmethod
    def row_to_line(self, row: tuple) -> str: ...
    @abstractmethod
    def line_to_row(self, line: str) -> tuple: ...

class BasicWordRepoTableSchema(IWordRepoTableSchema):
    def __init__(self, language: Language, table_prefix: str) -> None:
        super().__init__()
        self._language: Language = language
        self._table_prefix: str = table_prefix

    def table_name(self) -> str:
        return f"{self._table_prefix}_{self._language.lang_code}"

    def select_word(self, word: IBasicWord) -> str:
        return f"SELECT * FROM {self.table_name()} WHERE term = '{word.term}' and translation = '{word.translation}'"

    def select_all_words(self):
        return f"SELECT * FROM {self.table_name()}"

    def create_table(self, conn: Connection):  # protected table name
        pass

    def insert_word(self) -> str:
        pass

    def get_insert_params(self, word: IBasicWord) -> tuple:
        pass

    def row_to_line(self, row: tuple) -> str:
        pass

    def line_to_row(self, line: str) -> tuple:
        pass

class EnglishWordRepoTableSchema(BasicWordRepoTableSchema):
    def create_table(self, conn):  # protected table name
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name()} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            translation TEXT NOT NULL,
            transcription TEXT
        )
        """
        conn.execute(sql)

    def insert_word(self):
        return f"INSERT OR REPLACE INTO {self.table_name()} (term, translation, transcription) VALUES (?, ?, ?)"

    def get_insert_params(self, word):
        return word.term, word.translation, getattr(word, 'transcription', None)

    def row_to_line(self, row: tuple):
        term, translation, transcription = row
        return f"{term}|{translation}|{transcription or ''}"

    def line_to_row(self, line: str) -> tuple:
        parts = line.strip().split("|")
        term, translation, transcription = (parts + ["", ""])[:3]
        return term, translation, transcription