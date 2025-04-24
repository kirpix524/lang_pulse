from models.user_dictionary import UserDictionary
from models.language import Language
from models.session import Session
from models.user import User
from storage.interfaces import ISessionStorage


class SessionRepository:
    def __init__(self, storage: ISessionStorage):
        self._storage = storage
        self._user = None
        self._language = None
        self._dictionary = None
        self._sessions: list[Session] = []

    def __get_new_session_id(self) -> int:
        return max((session.get_id() for session in self._sessions), default=0) + 1

    def new_session(self) -> Session:
        session = Session(self._user, self._language, self.__get_new_session_id(), [])
        self._sessions.append(session)
        self._storage.save_all_sessions(self._user, self._language, self._sessions)
        return session

    def get_sessions(self) -> list[Session]:
        return self._sessions

    def set_session_context(self, user:User, language:Language, dictionary:UserDictionary) -> None:
        self._user = user
        self._language = language
        self._dictionary = dictionary
        self._sessions = self._storage.load_all_sessions(user, language, dictionary)
