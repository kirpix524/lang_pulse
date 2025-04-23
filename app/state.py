from models.session import Session
from models.user import User
from models.language import Language
from models.dictionary import Dictionary
from repositories.lang_repo import LanguageRepository
from repositories.session_repo import SessionRepository
from repositories.user_repo import UserRepository
from storage.interfaces import IDictionaryStorage, ISessionStorage, IStatsStorage, IUserStorage, ILanguageStorage
from storage.factory import create_storage

class AppState:
    user_storage: IUserStorage
    language_storage: ILanguageStorage
    dictionary_storage: IDictionaryStorage
    session_storage: ISessionStorage
    stats_storage: IStatsStorage

    def __init__(self):
        storage = create_storage()
        self.dictionary_storage = storage["dictionaries"]
        self.session_storage = storage["sessions"]
        self.stats_storage = storage["stats"]
        self.user_storage = storage["users"]
        self.language_storage = storage["languages"]
        self.__user_repo = UserRepository(self.user_storage)
        self.__lang_repo = LanguageRepository(self.language_storage)
        self.__session_repo = SessionRepository(self.session_storage)
        self.__user: User | None = None
        self.__language: Language | None = None
        self.__dictionary: Dictionary | None = None
        self.__session: Session | None = None


    def get_user_repo(self) -> UserRepository:
        return self.__user_repo

    def get_lang_repo(self) -> LanguageRepository:
        return self.__lang_repo

    def set_user(self, user: User) -> None:
        self.__user = user

    def get_user(self) -> User:
        return self.__user

    def set_language(self, language: Language) -> None:
        self.__language = language

    def get_language(self) -> Language:
        return self.__language

    def set_dictionary(self, dictionary: Dictionary) -> None:
        self.__dictionary = dictionary

    def get_dictionary(self) -> Dictionary:
        return self.__dictionary

    def set_session_repo(self, session_repo: SessionRepository) -> None:
        self.__session_repo = session_repo

    def get_session_repo(self) -> SessionRepository:
        return self.__session_repo

    def set_session(self, session: Session) -> None:
        self.__session = session

    def get_session(self) -> Session:
        return self.__session







