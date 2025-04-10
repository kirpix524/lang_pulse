from models.language import Language
from models.user import User
from models.word import Word

import storage.config as config

class DataBase:
    def __init__(self):
        pass

    def save_user_list(self, user_list: list[User]) -> None:
        pass

    def save_language_list(self, language_list: list[Language]) -> None:
        pass

    def save_word_list(self, word: Word, user: User) -> None:
        pass

    def load_user_list(self) -> list[User]:
        pass

    def load_language_list(self) -> list[Language]:
        pass

    def load_word_list(self, user:User) -> list[Word]:
        pass


class DBFile(DataBase):
    def __init__(self, file_names):
        super().__init__()
        self.file_names = file_names

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
                    language_id, language_code, language_name = line.split("|", 2)
                    language = Language(int(language_id.strip()), language_code.strip(), language_name.strip())
                    languages.append(language)
        except FileNotFoundError:
            print(f"Файл {self.file_names["LANGUAGES"]} не найден. Будет создан при сохранении.")

        return languages

    def save_language_list(self, language_list: list[Language]) -> None:
        with open(self.file_names["LANGUAGES"], "w", encoding="utf-8") as file:
            for language in language_list:
                file.write(f"{language.lang_id}|{language.lang_code}|{language.lang_name}\n")

db = DBFile(config.FILE_NAMES)

