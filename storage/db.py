from models.language import Language
from models.user import User
from models.dictionary import Word, Dictionary
from models.session import Session
from datetime import datetime

import storage.config as config

class DataBase:
    def __init__(self):
        pass

    def save_user_list(self, user_list: list[User]) -> None:
        pass

    def save_language_list(self, language_list: list[Language]) -> None:
        pass

    def save_dictionary(self, dictionary: Dictionary) -> None:
        pass

    def save_session(self, session: Session) -> None:
        pass

    def load_user_list(self) -> list[User]:
        pass

    def load_language_list(self) -> list[Language]:
        pass

    def load_dictionary(self, user: User, language: Language) -> Dictionary:
        pass

    def load_session_list(self, dictionary: Dictionary) -> list[Session]:
        pass

    def load_session(self, dictionary: Dictionary, session_id: int) -> Session:
        pass


def get_parts(line, count):
    parts = line.strip().split("|")
    # Дополнить список до 3 элементов значением None
    parts += [None] * (count - len(parts))
    return parts


class DBFile(DataBase):
    def __init__(self, file_names, dictionary_data, session_data):
        super().__init__()
        self.file_names = file_names
        self.dictionary_data = dictionary_data
        self.session_data = session_data

    def load_user_list(self) -> list[User]:
        users: list[User] = []
        try:
            with open(self.file_names["USERS"], "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    user_id, username = line.split("|", 1)
                    user = User(username.strip(), int(user_id.strip()))
                    users.append(user)
        except FileNotFoundError:
            print(f"Файл {self.file_names["USERS"]} не найден. Будет создан при сохранении.")

        return users

    def save_user_list(self, user_list: list[User]) -> None:
        with open(self.file_names["USERS"], "w", encoding="utf-8") as file:
            for user in user_list:
                file.write(f"{user.userid}|{user.username}\n")

    def load_language_list(self) -> list[Language]:
        languages: list[Language] = []
        try:
            with open(self.file_names["LANGUAGES"], "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    language_id, language_name, language_code = line.split("|", 2)
                    language = Language(int(language_id.strip()), language_code.strip(), language_name.strip())
                    languages.append(language)
        except FileNotFoundError:
            print(f"Файл {self.file_names["LANGUAGES"]} не найден. Будет создан при сохранении.")

        return languages

    def save_language_list(self, language_list: list[Language]) -> None:
        with open(self.file_names["LANGUAGES"], "w", encoding="utf-8") as file:
            for language in language_list:
                file.write(f"{language.lang_id}|{language.lang_code}|{language.lang_name}\n")

    def __get_sessions_list_file_name(self, user: User, language: Language) -> str:
        return (f"{self.session_data['LIST_DIRECTORY']}"
                + f"{self.session_data['LIST_FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")

    def __get_session_file_name(self, session_id: int) -> str:
        return (f"{self.session_data['DIRECTORY']}"
                + f"{self.session_data['FILE_NAME_PREFIX']}_{session_id}.txt")

    def load_session(self, dictionary: Dictionary, session_id: int) -> Session:
        session_file_name = self.__get_session_file_name(session_id)
        words: list[Word] = []
        try:
            with open(session_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    parts = get_parts(line, 2)
                    term, translation = parts
                    word = dictionary.get_word(term, translation)
                    if word:
                        words.append(word)
        except FileNotFoundError:
            print(f"Файл {session_file_name} не найден. Будет создан при сохранении.")

        return Session(dictionary, session_id, words)

    def save_session(self, session: Session) -> None:
        with open(self.__get_session_file_name(session.get_id()), "w", encoding="utf-8") as file:
            for word in session.get_words():
                file.write(f"{word.get_term()}|{word.get_translation()}\n")

    def load_session_list(self, dictionary:Dictionary) -> list[Session]:
        sessions_list_file_name = self.__get_sessions_list_file_name(dictionary.get_user(), dictionary.get_language())
        sessions: list[Session] = []
        sessions_tmp = []
        try:
            with open(sessions_list_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    parts = get_parts(line, 3)
                    session_id, created_at, last_repeated_at = parts
                    session = self.load_session(dictionary, int(session_id))
                    session.set_created_at(created_at)
                    session.set_last_repeated_at(last_repeated_at)
                    sessions.append(session)
        except FileNotFoundError:
            print(f"Файл {sessions_list_file_name} не найден. Будет создан при сохранении.")



        return sessions

    def save_session_list(self,dictionary:Dictionary, sessions: list[Session]) -> None:
        with open(self.__get_sessions_list_file_name(dictionary.get_user(), dictionary.get_language()), "w", encoding="utf-8") as file:
            for session in sessions:
                file.write(f"{session.get_id()}"
                           f"|{session.get_created_at() if session.get_created_at() else ''}"
                           f"|{session.get_last_repeated_at() if session.get_last_repeated_at() else ''}\n")

    def __get_dictionary_file_name(self, user: User, language: Language) -> str:
        return (f"{self.dictionary_data['DIRECTORY']}"
                + f"{self.dictionary_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")

    def load_dictionary(self, user: User, language: Language) -> Dictionary:
        dictionary = Dictionary(user, language)
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        words: list[Word] = []
        try:
            with open(dictionary_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    parts = get_parts(line, 5)
                    word, translation, transcription, added_at, last_repeated_at = parts
                    if (added_at is None)or (added_at==''): added_at = datetime.now()
                    words.append(Word(word, translation, transcription, added_at, last_repeated_at))
        except FileNotFoundError:
            print(f"Файл {dictionary_file_name} не найден. Будет создан при сохранении.")

        dictionary.set_words(words)
        return dictionary

    def save_dictionary(self, dictionary: Dictionary) -> None:
        user = dictionary.get_user()
        language = dictionary.get_language()
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        with open(dictionary_file_name, "w", encoding="utf-8") as file:
            for word in dictionary.get_words():
                file.write(f"{word.word}|{word.translation}"
                           f"|{word.transcription if word.transcription else ''}"
                           f"|{word.added_at if word.added_at else ''}"
                           f"|{word.last_repeated_at if word.last_repeated_at else ''}\n")

db = DBFile(config.FILE_NAMES, config.DICTIONARY_DATA, config.SESSION_DATA)

