from models.dictionary import Dictionary
from models.session import Session
from storage.db import db

class SessionRepository:
    def __init__(self, dictionary: Dictionary):
        self.__sessions: list[Session] = db.load_session_list(dictionary)
        self.__dictionary = dictionary

    def __get_new_session_id(self) -> int:
        return len(self.__sessions) + 1

    def new_session(self) -> Session:
        session = Session(self.__dictionary, self.__get_new_session_id(), [])
        self.__sessions.append(session)
        db.save_session_list(self.__dictionary, self.__sessions)
        db.save_session(session)
        return session

    def get_sessions(self) -> list[Session]:
        return self.__sessions