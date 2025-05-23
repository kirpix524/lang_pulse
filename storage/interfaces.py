from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from models.language import Language
from models.session import Session, Training
from models.user import User
from models.user_word import IBasicUserWord
from models.word import IBasicWord

if TYPE_CHECKING:
    from models.user_dictionary import UserDictionary
    from repositories.word_repo import WordRepository


class IUserStorage(ABC):
    @abstractmethod
    def load_user_list(self) -> list[User]:
        pass

    @abstractmethod
    def save_user_list(self, user_list: list[User]) -> None:
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass


class ILanguageStorage(ABC):
    @abstractmethod
    def load_language_list(self) -> list[Language]:
        pass

    @abstractmethod
    def save_language_list(self, language_list: list[Language]) -> None:
        pass

    @abstractmethod
    def save_language(self, language: Language) -> None:
        pass


class IWordStorage(ABC):
    @abstractmethod
    def load_word_list(self, language: Language) -> list[IBasicUserWord]:
        pass

    @abstractmethod
    def save_word_list(self, words: list[IBasicWord], language: Language) -> None:
        pass

    @abstractmethod
    def save_word(self, word: IBasicWord, language: Language) -> None:
        pass


class IUserDictionaryStorage(ABC):
    @abstractmethod
    def load_dictionary(self, user: User, language: Language, word_repo: "WordRepository") -> "UserDictionary":
        pass

    @abstractmethod
    def save_dictionary(self, dictionary: "UserDictionary") -> None:
        pass


class ISessionStorage(ABC):
    @abstractmethod
    def load_all_sessions(self, user: User, language: Language, dictionary: "UserDictionary") -> list[Session]:
        pass

    @abstractmethod
    def save_all_sessions(self, user: User, language: Language, sessions: list[Session]) -> None:
        pass


class IStatsStorage(ABC):
    @abstractmethod
    def save_training_stats(self, session: Session, training: Training) -> None:
        pass

    @abstractmethod
    def load_training_stats_words(self, user: User, language: Language, dictionary: "UserDictionary") -> None:
        pass
