import sqlite3
from sqlite3 import Connection
from datetime import datetime

from app.config import TrainingDirection
from models.user_dictionary import UserDictionary
from models.language import Language
from models.session import Session
from models.user import User
from storage.interfaces import ISessionStorage

class SessionSQLiteStorage(ISessionStorage):
    def __init__(self, sql_data: dict[str, str]) -> None:
        self._conn: Connection = sqlite3.connect(sql_data['db_path'])
        self._conn.row_factory = sqlite3.Row
        self._sql_data = sql_data

    def __get_sessions_table_name(self, language: Language) -> str:
        return f"{self._sql_data['sessions_table_prefix']}_{language.lang_code}".lower()

    def __get_words_table_name(self, language: Language) -> str:
        return f"{self._sql_data['session_words_table_prefix']}_{language.lang_code}".lower()

    def __get_trainings_table_name(self, language: Language) -> str:
        return f"{self._sql_data['trainings_table_prefix']}_{language.lang_code}".lower()

    def __ensure_tables(self, language: Language) -> None:
        sessions_table = self.__get_sessions_table_name(language)
        words_table = self.__get_words_table_name(language)
        trainings_table = self.__get_trainings_table_name(language)

        self._conn.execute(
            f"CREATE TABLE IF NOT EXISTS {sessions_table} ("
            "id INTEGER PRIMARY KEY, "
            "user_id INTEGER, "
            "created_at TEXT"
            ")"
        )
        self._conn.execute(
            f"CREATE TABLE IF NOT EXISTS {words_table} ("
            "session_id INTEGER, "
            "term TEXT NOT NULL, "
            "translation TEXT NOT NULL"
            ")"
        )
        self._conn.execute(
            f"CREATE TABLE IF NOT EXISTS {trainings_table} ("
            "session_id INTEGER, "
            "training_id INTEGER, "
            "direction TEXT NOT NULL, "
            "interval REAL NOT NULL, "
            "training_date_time TEXT NOT NULL"
            ")"
        )
        self._conn.commit()

    def load_all_sessions(
        self,
        user: User,
        language: Language,
        dictionary: UserDictionary
    ) -> list[Session]:
        self.__ensure_tables(language)
        sessions_table = self.__get_sessions_table_name(language)
        words_table = self.__get_words_table_name(language)
        trainings_table = self.__get_trainings_table_name(language)

        query = (
            f"SELECT "
            f"s.id AS session_id, "
            f"s.created_at AS created_at, "
            f"w.term AS term, "
            f"w.translation AS translation, "
            f"t.training_id AS training_id, "
            f"t.direction AS direction, "
            f"t.interval AS interval, "
            f"t.training_date_time AS training_date_time "
            f"FROM {sessions_table} s "
            f"LEFT JOIN {words_table} w ON s.id = w.session_id "
            f"LEFT JOIN {trainings_table} t ON s.id = t.session_id "
            f"WHERE s.user_id = ? "
            f"ORDER BY s.id"
        )
        cursor = self._conn.execute(query, (user.userid,))
        sessions_map: dict[int, Session] = {}

        for row in cursor.fetchall():
            session_id: int = row['session_id']
            if session_id not in sessions_map:
                created_at_str: str = row['created_at']
                created_at: datetime = (
                    datetime.fromisoformat(created_at_str)
                    if created_at_str
                    else datetime.now()
                )
                session = Session(user, language, session_id, [])
                session.set_created_at(created_at)
                sessions_map[session_id] = session

            # Add word if present
            term = row['term']
            translation = row['translation']
            if term is not None and translation is not None:
                word = dictionary.find_word(term, translation)
                if word:
                    sessions_map[session_id].add_words([word])

            # Add training if present
            training_id = row['training_id']
            if training_id is not None:
                direction = TrainingDirection(row['direction'])
                interval: float = row['interval']
                training_date_time = datetime.fromisoformat(row['training_date_time'])
                sessions_map[session_id].add_existing_training(
                    direction,
                    interval,
                    training_id,
                    training_date_time
                )

        return list(sessions_map.values())

    def save_all_sessions(
        self,
        user: User,
        language: Language,
        sessions: list[Session]
    ) -> None:
        self.__ensure_tables(language)
        sessions_table = self.__get_sessions_table_name(language)
        words_table = self.__get_words_table_name(language)
        trainings_table = self.__get_trainings_table_name(language)

        # Delete old sessions for user
        self._conn.execute(f"DELETE FROM {sessions_table} WHERE user_id = ?", (user.userid,))
        self._conn.execute(
            f"DELETE FROM {words_table} WHERE session_id IN (SELECT id FROM {sessions_table} WHERE user_id = ?)"
            , (user.userid,)
        )
        self._conn.execute(
            f"DELETE FROM {trainings_table} WHERE session_id IN (SELECT id FROM {sessions_table} WHERE user_id = ?)"
            , (user.userid,)
        )

        # Insert sessions and related data
        for session in sessions:
            params_sessions = (
                session.get_id(),
                user.userid,
                session.get_created_at().isoformat() if session.get_created_at() else ''
            )
            self._conn.execute(
                f"INSERT INTO {sessions_table} (id, user_id, created_at) VALUES (?, ?, ?)"
                , params_sessions
            )
            for word in session.get_words():
                params_word = (
                    session.get_id(),
                    word.word.term,
                    word.word.translation
                )
                self._conn.execute(
                    f"INSERT INTO {words_table} (session_id, term, translation) VALUES (?, ?, ?)"
                    , params_word
                )
            for training in session.get_trainings():
                params_tr = (
                    session.get_id(),
                    training.get_id(),
                    training.get_direction_value(),
                    training.interval,
                    training.training_date_time.isoformat()
                )
                self._conn.execute(
                    f"INSERT INTO {trainings_table} (session_id, training_id, direction, interval, training_date_time) VALUES (?, ?, ?, ?, ?)"
                    , params_tr
                )
        self._conn.commit()


