from models.dictionary import Dictionary
from models.session import Session
from storage.db import db

class SessionRepository:
    def __init__(self, dictionary: Dictionary):
        self.sessions: list[Session] = db.load_session_list(dictionary)