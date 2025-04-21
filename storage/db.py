from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from models.language import Language
from models.user import User
from models.dictionary import EnglishWord, Dictionary, WordInterface
from models.session import Session, Training
from storage.config import TrainingDirection

import storage.config as config
from stats.stats import StatsRow


class DataBase:
    @abstractmethod
    def load_user_list(self) -> list[User]:
        pass

    @abstractmethod
    def save_user_list(self, user_list: list[User]) -> None:
        pass

    @abstractmethod
    def load_language_list(self) -> list[Language]:
        pass

    @abstractmethod
    def save_language_list(self, language_list: list[Language]) -> None:
        pass

    @abstractmethod
    def load_dictionary(self, user: User, language: Language) -> Dictionary:
        pass

    @abstractmethod
    def save_dictionary(self, dictionary: Dictionary) -> None:
        pass

    @abstractmethod
    def load_all_sessions(self, dictionary: Dictionary) -> list[Session]:
        pass

    @abstractmethod
    def save_all_sessions(self, dictionary: Dictionary, sessions: list[Session]) -> None:
        pass

    @abstractmethod
    def save_training_stats(self, session: Session, training: Training):
        pass

    @abstractmethod
    def load_training_stats_words(self, dictionary: Dictionary):
        pass


def get_parts(line, count):
    parts = line.strip().split("|")
    # Дополнить список до 3 элементов значением None
    parts += [None] * (count - len(parts))
    return parts


class DBFile(DataBase):
    def __init__(self, file_names, dictionary_data, session_data, stats_data):
        super().__init__()
        self.__file_names = file_names
        self.__dictionary_data = dictionary_data
        self.__session_data = session_data
        self.__stats_data = stats_data

    def load_user_list(self) -> list[User]:
        users: list[User] = []
        try:
            with open(self.__file_names["USERS"], "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    user_id, username = line.split("|", 1)
                    user = User(username.strip(), int(user_id.strip()))
                    users.append(user)
        except FileNotFoundError:
            print(f"Файл {self.__file_names["USERS"]} не найден. Будет создан при сохранении.")

        return users

    def save_user_list(self, user_list: list[User]) -> None:
        with open(self.__file_names["USERS"], "w", encoding="utf-8") as file:
            for user in user_list:
                file.write(f"{user.userid}|{user.username}\n")

    def load_language_list(self) -> list[Language]:
        languages: list[Language] = []
        try:
            with open(self.__file_names["LANGUAGES"], "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    language_id, language_name, language_code = line.split("|", 2)
                    language = Language(int(language_id.strip()), language_code.strip(), language_name.strip())
                    languages.append(language)
        except FileNotFoundError:
            print(f"Файл {self.__file_names["LANGUAGES"]} не найден. Будет создан при сохранении.")

        return languages

    def save_language_list(self, language_list: list[Language]) -> None:
        with open(self.__file_names["LANGUAGES"], "w", encoding="utf-8") as file:
            for language in language_list:
                file.write(f"{language.lang_id}|{language.lang_code}|{language.lang_name}\n")

    def __get_sessions_file_name(self, user: User, language: Language) -> str:
        file_path = (f"{self.__session_data['DIRECTORY']}"
                + f"{self.__session_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def load_all_sessions(self, dictionary: Dictionary) -> list[Session]:
        sessions_file = self.__get_sessions_file_name(dictionary.get_user(), dictionary.get_language())
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
                            sessions[session_id].add_existing_training(direction, interval, training_id, datetime.fromisoformat(training_date_time))

        except FileNotFoundError:
            print(f"Файл {sessions_file} не найден. Будет создан при сохранении.")

        return list(sessions.values())

    def save_all_sessions(self, dictionary: Dictionary, sessions: list[Session]) -> None:
        sessions_file = self.__get_sessions_file_name(dictionary.get_user(), dictionary.get_language())

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

    def __get_dictionary_file_name(self, user: User, language: Language) -> str:
        file_path = (f"{self.__dictionary_data['DIRECTORY']}"
                + f"{self.__dictionary_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def load_dictionary(self, user: User, language: Language) -> Dictionary:
        dictionary = Dictionary(user, language)
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        words: list[WordInterface] = []
        try:
            with open(dictionary_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    word, translation, transcription, added_at = (parts + [""] * 4)[:4]
                    if added_at:
                        added_at = datetime.fromisoformat(added_at)
                    else:
                        added_at = datetime.now()
                    words.append(EnglishWord(word, translation, transcription, added_at))
        except FileNotFoundError:
            print(f"Файл {dictionary_file_name} не найден. Будет создан при сохранении.")
        dictionary.set_words(words)
        self.load_training_stats_words(dictionary)
        return dictionary

    def save_dictionary(self, dictionary: Dictionary) -> None:
        user = dictionary.get_user()
        language = dictionary.get_language()
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        with open(dictionary_file_name, "w", encoding="utf-8") as file:
            for word in dictionary.get_words():
                file.write(f"{word.word}|{word.translation}"
                           f"|{word.get_transcription()}"
                           f"|{word.get_added_at()}\n")

    def __get_stats_file_name(self, user: User, language: Language) -> str:
        file_path = (f"{self.__stats_data['DIRECTORY']}"
                + f"{self.__stats_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def save_training_stats(self, session: Session, training: Training):
        """
        Сохраняет статистику тренировки в файл. Каждый элемент stats — это словарь с ключами:
        word, translation, success, recall_time, timestamp, direction
        """
        stats = training.get_stats()
        file_path = self.__get_stats_file_name(session.get_user(), session.get_language())

        with open(file_path, "a", encoding="utf-8") as f:
            for stat in stats:
                line = "T|" + "|".join([
                    str(stat.session_id),
                    str(stat.training_id),
                    str(stat.word),
                    str(stat.translation),
                    "1" if stat.success else "0",
                    f"{stat.recall_time:.2f}" if stat.recall_time is not None else "",
                    str(stat.timestamp),
                    stat.get_direction_value()
                ])
                f.write(line + "\n")

    def load_training_stats_words(self, dictionary: Dictionary):
        def parse_direction(value: str) -> TrainingDirection | None:
            try:
                return TrainingDirection(value)
            except ValueError:
                return None  # или выбросить исключение, если нужно строго

        file_path = self.__get_stats_file_name(dictionary.get_user(), dictionary.get_language())
        words = dictionary.get_words()
        word_keys = {(w.word, w.translation) for w in words}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("T|"):
                        continue
                    parts = line.strip().split("|")
                    if len(parts) < 8:
                        continue
                    # гарантируем, что будет 9 элементов
                    _, session_id, training_id, word, translation, success, recall_time, timestamp, direction = (parts + [""] * 9)[:9]

                    if (word, translation) not in word_keys:
                        continue

                    word_obj = dictionary.find_word(word, translation)
                    if not word_obj:
                        continue

                    stat = StatsRow(
                        word=word,
                        translation=translation,
                        session_id=int(session_id),
                        training_id=int(training_id),
                        success=(success == "1"),
                        recall_time=float(recall_time) if recall_time else None,
                        timestamp=datetime.fromisoformat(timestamp) if timestamp else None,
                        direction=parse_direction(direction)
                    )

                    word_obj.add_stat(stat)

        except FileNotFoundError:
            print(f"Статистика не найдена: {file_path}")



db = DBFile(config.FILE_NAMES, config.DICTIONARY_DATA, config.SESSIONS_DATA, config.STATS_DATA)

