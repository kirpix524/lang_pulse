from models.language import Language
from models.user import User
from stats.stats import StatsRow
from utils.utils import parse_datetime

class Word:
    def __init__(self, word, translation, transcription=None, added_at=None, last_repeated_at=None):
        self.word = word
        self.translation = translation
        self.__transcription = transcription

        # Преобразование строк в datetime, если они заданы как строки
        self.__added_at = parse_datetime(added_at)
        self.__last_repeated_at = parse_datetime(last_repeated_at)
        self.__start_time = None
        self.__stats = []

    def get_start_time(self):
        return self.__start_time

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def get_added_at(self):
        return self.__added_at

    def set_added_at(self, added_at):
        self.__added_at = parse_datetime(added_at)

    def get_last_repeated_at(self):
        return self.__last_repeated_at

    def set_last_repeated_at(self, last_repeated_at):
        self.__last_repeated_at = parse_datetime(last_repeated_at)

    def get_transcription(self):
        return self.__transcription if self.__transcription else ''

    def add_stat(self, stat: StatsRow | dict):
        if isinstance(stat, dict):
            stat = StatsRow.from_dict(stat)
        self.__stats.append(stat)

    def get_stats(self) -> list[StatsRow]:
        return self.__stats

class Dictionary:
    def __init__(self, user: User, language: Language):
        self.__user = user
        self.__language = language
        self.__words: list[Word] = []

    def set_user(self, user: User):
        self.__user = user

    def set_language(self, language: Language):
        self.__language = language

    def set_words(self, words: list[Word]):
        self.__words = words

    def get_user(self):
        return self.__user

    def get_language(self):
        return self.__language

    def get_words(self):
        return self.__words

    def get_word(self, word, translation):
        for w in self.__words:
            if w.word == word and w.translation == translation:
                return w
        return None

    def add_word(self, word: Word):
        # Проверяем, есть ли уже такое сочетание слово + перевод
        for w in self.__words:
            if w.word == word.word and w.translation == word.translation:
                return  # Не добавляем дубликат
        self.__words.append(word)