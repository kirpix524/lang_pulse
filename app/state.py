from models.session import Session
from models.user import User
from models.language import Language
from models.user_dictionary import UserDictionary


class AppState:
    def __init__(self):
        self.__user: User | None = None
        self.__language: Language | None = None
        self.__dictionary: UserDictionary | None = None
        self.__session: Session | None = None

    def set_user(self, user: User) -> None:
        self.__user = user

    def get_user(self) -> User:
        return self.__user

    def set_language(self, language: Language) -> None:
        self.__language = language

    def get_language(self) -> Language:
        return self.__language

    def set_dictionary(self, dictionary: UserDictionary) -> None:
        self.__dictionary = dictionary

    def get_dictionary(self) -> UserDictionary:
        return self.__dictionary

    def set_session(self, session: Session) -> None:
        self.__session = session

    def get_session(self) -> Session:
        return self.__session







