from models.dictionary import Dictionary
from models.language import Language
from models.session import Session
from models.user import User
from storage.interfaces import ISessionStorage


class SessionRepository:
    def __init__(self, user: User, language: Language, storage: ISessionStorage, dictionary: Dictionary):
        self.__storage = storage
        self.__user = user
        self.__language = language
        self.__dictionary = dictionary
        self.__sessions: list[Session] = self.__storage.load_all_sessions(user, language, dictionary)

    def __get_new_session_id(self) -> int:
        return max((session.get_id() for session in self.__sessions), default=0) + 1

    def new_session(self) -> Session:
        session = Session(self.__user, self.__language, self.__get_new_session_id(), [])
        self.__sessions.append(session)
        self.__storage.save_all_sessions(self.__user, self.__language, self.__sessions)
        return session

    def get_sessions(self) -> list[Session]:
        return self.__sessions
