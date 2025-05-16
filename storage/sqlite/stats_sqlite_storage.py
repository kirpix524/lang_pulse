import sqlite3
from sqlite3 import Connection
from datetime import datetime

from app.config import TrainingDirection
from models.user_dictionary import UserDictionary
from models.language import Language
from models.session import Session, Training
from models.stats import StatsRow
from models.user import User
from storage.interfaces import IStatsStorage


class StatsSQLiteStorage(IStatsStorage):
    def __init__(self, sql_data: dict[str, str]) -> None:
        self._conn: Connection = sqlite3.connect(sql_data['db_path'])
        self._conn.row_factory = sqlite3.Row
        self._sql_data = sql_data

    def __get_stats_table_name(self, language: Language) -> str:
        return f"{self._sql_data['stats_table_prefix']}_{language.lang_code}".lower()

    def __ensure_table(self, language: Language) -> None:
        table = self.__get_stats_table_name(language)
        self._conn.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ("
            "user_id INTEGER, "
            "session_id INTEGER, "
            "training_id INTEGER, "
            "term TEXT NOT NULL, "
            "translation TEXT NOT NULL, "
            "success INTEGER NOT NULL, "
            "recall_time REAL, "
            "timestamp TEXT, "
            "direction TEXT"
            ")"
        )
        self._conn.commit()

    def save_training_stats(self, session: Session, training: Training) -> None:
        stats = training.get_stats()
        table = self.__get_stats_table_name(session.get_language())
        self.__ensure_table(session.get_language())

        with self._conn:
            for stat in stats:
                params = (
                    session.get_user().userid,
                    stat.session_id,
                    stat.training_id,
                    stat.term,
                    stat.translation,
                    1 if stat.success else 0,
                    stat.recall_time,
                    stat.timestamp.isoformat() if stat.timestamp else None,
                    stat.get_direction_value()
                )
                self._conn.execute(
                    f"INSERT INTO {table} "
                    "(user_id, session_id, training_id, term, translation, success, recall_time, timestamp, direction) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    params
                )

    def load_training_stats_words(
        self,
        user: User,
        language: Language,
        dictionary: UserDictionary
    ) -> None:
        def parse_direction(value: str) -> TrainingDirection | None:
            try:
                return TrainingDirection(value)
            except ValueError:
                return None

        table = self.__get_stats_table_name(language)
        self.__ensure_table(language)

        words = dictionary.get_words()
        word_keys = {(w.word.term, w.word.translation) for w in words}

        cursor = self._conn.execute(
            f"SELECT session_id, training_id, term, translation, success, recall_time, timestamp, direction "
            f"FROM {table} WHERE user_id = ?",
            (user.userid,)
        )

        for row in cursor.fetchall():
            term: str = row["term"]
            translation: str = row["translation"]
            if (term, translation) not in word_keys:
                continue

            word_obj = dictionary.find_word(term, translation)
            if not word_obj:
                continue

            stat = StatsRow(
                term=term,
                translation=translation,
                session_id=row["session_id"],
                training_id=row["training_id"],
                success=bool(row["success"]),
                recall_time=row["recall_time"],
                timestamp=datetime.fromisoformat(row["timestamp"]) if row["timestamp"] else None,
                direction=parse_direction(row["direction"])
            )
            word_obj.add_stat(stat)
