from models.language import Language
from models.user import User
from models.dictionary import Word, Dictionary

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

    def load_user_list(self) -> list[User]:
        pass

    def load_language_list(self) -> list[Language]:
        pass

    def load_dictionary(self, dictionary:Dictionary) -> list[Word]:
        pass


class DBFile(DataBase):
    def __init__(self, file_names, dictionary_data):
        super().__init__()
        self.file_names = file_names
        self.dictionary_data = dictionary_data

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

    def __get_dictionary_file_name(self, user: User, language: Language) -> str:
        return f"{self.dictionary_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt"

    def load_dictionary(self, dictionary:Dictionary) -> list[Word]:
        user = dictionary.get_user()
        language = dictionary.get_language()
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        words: list[Word] = []
        try:
            with open(dictionary_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    word, translation, transcription = line.split("|", 3)
                    words.append(Word(word.strip(), translation.strip(), transcription.strip()))
        except FileNotFoundError:
            print(f"Файл {self.file_names['DICTIONARY']} не найден. Будет создан при сохранении.")

        return words

    def save_dictionary(self, dictionary: Dictionary) -> None:
        user = dictionary.get_user()
        language = dictionary.get_language()
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        with open(dictionary_file_name, "w", encoding="utf-8") as file:
            for word in dictionary.get_words():
                file.write(f"{word.word}|{word.translation}|{word.transcription}\n")

db = DBFile(config.FILE_NAMES, config.DICTIONARY_DATA)

