from abc import abstractmethod
from datetime import datetime

from models.stats import StatsRow
from models.word import IBasicWord, EnglishWord


class IBasicUserWord:
    word: IBasicWord
    @abstractmethod
    def get_start_time(self) -> float:
        pass

    @abstractmethod
    def set_start_time(self, start_time: float) -> None:
        pass

    @abstractmethod
    def get_added_at(self) -> datetime:
        pass

    @abstractmethod
    def get_added_at_str(self, fmt: str = "%d.%m.%Y") -> str:
        pass

    @abstractmethod
    def get_last_repeated_at(self) -> datetime:
        pass

    @abstractmethod
    def get_last_repeated_at_str(self, fmt: str = "%d.%m.%Y") -> str:
        pass

    @abstractmethod
    def add_stat(self, stat: StatsRow) -> None:
        pass

    @abstractmethod
    def get_stats(self) -> list[StatsRow]:
        pass

class BasicUserWord(IBasicUserWord):
    def __init__(self, word: IBasicWord, added_at: datetime=None):
        self.word: IBasicWord = word
        self.__added_at = added_at
        self.__start_time = None
        self.__stats: list[StatsRow] = []

    def get_start_time(self):
        return self.__start_time

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def get_added_at(self):
        return self.__added_at

    def get_added_at_str(self, fmt: str = "%d.%m.%Y"):
        if not self.__added_at:
            return ''
        return self.__added_at.strftime(fmt)

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

    def add_stat(self, stat: StatsRow):
        self.__stats.append(stat)

    def get_stats(self) -> list[StatsRow]:
        return self.__stats

class EnglishUserWord(BasicUserWord):
    def __init__(self, word: EnglishWord, added_at: datetime = None):
        super().__init__(word, added_at)
        self.word: EnglishWord = word  # просто аннотация типа