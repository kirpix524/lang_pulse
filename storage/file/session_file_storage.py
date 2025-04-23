from datetime import datetime
from pathlib import Path

from app.config import TrainingDirection
from models.user_dictionary import UserDictionary
from models.language import Language
from models.session import Session
from models.user import User
from storage.interfaces import ISessionStorage


class SessionFileStorage(ISessionStorage):
    def __init__(self, session_data: dict[str, str]):
        self.__session_data = session_data

    def __get_sessions_file_name(self, user: User, language: Language) -> str:
        file_path = (f"{self.__session_data['DIRECTORY']}"
                     + f"{self.__session_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def load_all_sessions(self, user: User, language: Language, dictionary: UserDictionary) -> list[Session]:
        sessions_file = self.__get_sessions_file_name(user, language)
        sessions: dict[int, Session] = {}

        try:
            with open(sessions_file, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if not parts:
                        continue

                    record_type = parts[0]

                    if record_type == "S" and len(parts) >= 3:
                        session_id = int(parts[1])
                        created_at = parts[2] if parts[2] else None

                        session = Session(dictionary.get_user(), dictionary.get_language(), session_id, [])
                        session.set_created_at(datetime.fromisoformat(created_at))
                        sessions[session_id] = session

                    elif record_type == "W" and len(parts) >= 4:
                        session_id = int(parts[1])
                        term = parts[2]
                        translation = parts[3]
                        word = dictionary.find_word(term, translation)
                        if word and session_id in sessions:
                            sessions[session_id].add_words([word])
                    elif record_type == "T" and len(parts) >= 6:
                        session_id = int(parts[1])
                        training_id = int(parts[2])
                        direction = TrainingDirection(parts[3])
                        interval = float(parts[4])
                        training_date_time = parts[5]

                        if session_id in sessions:
                            sessions[session_id].add_existing_training(direction, interval, training_id,
                                                                       datetime.fromisoformat(training_date_time))

        except FileNotFoundError:
            print(f"Файл {sessions_file} не найден. Будет создан при сохранении.")

        return list(sessions.values())

    def save_all_sessions(self, user: User, language: Language, sessions: list[Session]) -> None:
        sessions_file = self.__get_sessions_file_name(user, language)

        with open(sessions_file, "w", encoding="utf-8") as file:
            for session in sessions:
                file.write(
                    f"S|{session.get_id()}|{session.get_created_at() or ''}\n"
                )
                for word in session.get_words():
                    file.write(
                        f"W|{session.get_id()}|{word.word}|{word.translation}\n"
                    )
                for training in session.get_trainings():
                    file.write(
                        f"T|{session.get_id()}|{training.get_id()}|{training.get_direction_value()}|"
                        f"{training.get_interval()}|{training.get_training_date_time()}\n"
                    )
