from abc import abstractmethod

from models.dictionary import Dictionary
from models.language import Language
from models.session import Session, Training
from models.user import User


class IUserStorage:
    @abstractmethod
    def load_user_list(self) -> list[User]:
        pass

    @abstractmethod
    def save_user_list(self, user_list: list[User]) -> None:
        pass


class ILanguageStorage:
    @abstractmethod
    def load_language_list(self) -> list[Language]:
        pass

    @abstractmethod
    def save_language_list(self, language_list: list[Language]) -> None:
        pass


class IDictionaryStorage:
    @abstractmethod
    def load_dictionary(self, user: User, language: Language) -> Dictionary:
        pass

    @abstractmethod
    def save_dictionary(self, dictionary: Dictionary) -> None:
        pass


class ISessionStorage:
    @abstractmethod
    def load_all_sessions(self, user: User, language: Language, dictionary: Dictionary) -> list[Session]:
        pass

    @abstractmethod
    def save_all_sessions(self, user: User, language: Language, sessions: list[Session]) -> None:
        pass


class IStatsStorage:
    @abstractmethod
    def save_training_stats(self, session: Session, training: Training):
        pass

    @abstractmethod
    def load_training_stats_words(self, user: User, language: Language, dictionary: Dictionary):
        pass
