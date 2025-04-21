from models.session import Session
from models.user import User
from models.language import Language
from models.dictionary import Dictionary
from storage.lang_repo import LanguageRepository
from storage.session_repo import SessionRepository
from storage.user_repo import UserRepository

class AppState:
    def __init__(self):
        self.__user_repo = UserRepository()
        self.__lang_repo = LanguageRepository()
        self.__user: User | None = None
        self.__language: Language | None = None
        self.__dictionary: Dictionary | None = None
        self.__session_repo: SessionRepository | None = None
        self.__session: Session | None = None

    def get_user_repo(self) -> UserRepository:
        return self.__user_repo

    def get_lang_repo(self) -> LanguageRepository:
        return self.__lang_repo

    def set_user(self, user: User):
        self.__user = user

    def get_user(self) -> User:
        return self.__user

    def set_language(self, language: Language):
        self.__language = language

    def get_language(self) -> Language:
        return self.__language

    def set_dictionary(self, dictionary: Dictionary):
        self.__dictionary = dictionary

    def get_dictionary(self) -> Dictionary:
        return self.__dictionary

    def set_session_repo(self, session_repo: SessionRepository):
        self.__session_repo = session_repo

    def get_session_repo(self) -> SessionRepository:
        return self.__session_repo

    def set_session(self, session: Session):
        self.__session = session

    def get_session(self) -> Session:
        return self.__session







