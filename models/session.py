from datetime import datetime
from utils.utils import parse_datetime
from models.dictionary import Dictionary, Word


class Session:
    def __init__(self, dictionary: Dictionary, session_id: int, words: list[Word]):
        self.__dictionary = dictionary
        self.__session_id = session_id
        self.__words = words
        self.__created_at = datetime.now()
        self.__last_repeated_at = None

    def add_words(self, words: list[Word]):
        for word in words:
            self.__words.append(word)

    def get_words(self) -> list[Word]:
        return self.__words

    def get_id(self):
        return self.__session_id

    def get_session_name(self):
        return f"Session {self.__session_id}"

    def get_created_at(self):
        return parse_datetime(self.__created_at)

    def get_last_repeated_at(self):
        return parse_datetime(self.__last_repeated_at)

    def set_created_at(self, created_at):
        self.__created_at = created_at

    def set_last_repeated_at(self, last_repeated_at):
        self.__last_repeated_at = last_repeated_at

    def get_words_not_in_session(self) -> list[Word]:
        existing_words = {w.word for w in self.__words}
        return [w for w in self.__dictionary.get_words() if w.word not in existing_words]