from abc import ABC, abstractmethod
from models.language import Language
from models.user import User
from stats.stats import StatsRow
from utils.utils import parse_datetime
from datetime import datetime

class WordInterface:
    word: str
    translation: str
    @abstractmethod
    def get_start_time(self):
        pass
    
    @abstractmethod
    def set_start_time(self, start_time):
        pass
    
    @abstractmethod
    def get_added_at(self) -> datetime:
        pass
    
    @abstractmethod
    def set_added_at(self, added_at: datetime):
        pass
    
    @abstractmethod
    def get_last_repeated_at(self) -> datetime:
        pass

    @abstractmethod
    def get_last_repeated_at_str(self, fmt: str = "%d.%m.%Y") -> str:
        pass

    @abstractmethod
    def get_transcription(self) -> str:
        pass
    
    @abstractmethod
    def add_stat(self, stat: StatsRow) -> None:
        pass
    
    @abstractmethod
    def get_stats(self) -> list[StatsRow]:
        pass

class WordFactory:
    registry = {}

    @classmethod
    def register(cls, language: str, word_class):
        cls.registry[language.lower()] = word_class

    @classmethod
    def create_word(cls, language: str, *args, **kwargs) -> WordInterface:
        word_class = cls.registry.get(language.lower())
        if not word_class:
            raise ValueError(f"No Word class registered for language: {language}")
        return word_class(*args, **kwargs)

class BasicWord(WordInterface):
    def __init__(self, word, translation, transcription=None, added_at=None):
        self.word = word
        self.translation = translation
        self.__transcription = transcription
        self.__added_at = parse_datetime(added_at)
        self.__start_time = None
        self.__stats: list[StatsRow] = []

    def get_start_time(self):
        return self.__start_time

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def get_added_at(self):
        return self.__added_at

    def set_added_at(self, added_at):
        self.__added_at = parse_datetime(added_at)

    def get_last_repeated_at(self):
        if not self.__stats:
            return None
        latest = max(self.__stats, key=lambda s: s.timestamp)
        return latest.timestamp

    def get_last_repeated_at_str(self, fmt: str = "%d.%m.%Y"):
        last_repeated_at = self.get_last_repeated_at()
        if not last_repeated_at:
            return ''
        return last_repeated_at.strftime(fmt)

    def get_transcription(self):
        return self.__transcription if self.__transcription else ''

    def add_stat(self, stat: StatsRow):
        self.__stats.append(stat)

    def get_stats(self) -> list[StatsRow]:
        return self.__stats


class EnglishWord(BasicWord):
    def __init__(self, word, translation, transcription=None, added_at=None):
        super().__init__(word, translation, transcription=transcription, added_at=added_at)

class Dictionary:
    def __init__(self, user: User, language: Language):
        self.__user = user
        self.__language = language
        self.__words: list[WordInterface] = []

    def set_words(self, words: list[WordInterface]):
        self.__words = words

    def get_user(self):
        return self.__user

    def get_language(self):
        return self.__language

    def get_words(self):
        return self.__words

    def find_word(self, word, translation):
        for w in self.__words:
            if w.word == word and w.translation == translation:
                return w
        return None

    def add_word(self, word, translation, *args, **kwargs):
        # Проверяем, есть ли уже такое сочетание слово + перевод
        if self.find_word(word, translation):
            return # Не добавляем дубликат
        word = WordFactory.create_word(self.__language.lang_code, word, translation, added_at=datetime.now(), *args, **kwargs)
        self.__words.append(word)

    def update_training_stats(self, stats: list[StatsRow]):
        for stat in stats:
            word = self.find_word(str(stat.word), str(stat.translation))
            if not word:
                continue
            word.add_stat(stat)