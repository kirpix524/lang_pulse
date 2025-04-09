from models.user import User
from models.word import Word

import storage.config as config

class DataBase:
    def __init__(self):
        pass

    def save_user_list(self, user_list: list[User]) -> None:
        pass

    def save_word(self, word: Word, user: User) -> None:
        pass

    def load_user_list(self) -> list[User]:
        pass

    def load_word_list(self, user:User) -> list[Word]:
        pass


class DBFile(DataBase):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def load_user_list(self) -> list[User]:
        users: list[User] = []
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    user_id, username = line.split("|", 1)
                    user = User(username.strip(), int(user_id.strip()))
                    users.append(user)
        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден. Будет создан при сохранении.")

        return users

    def save_user_list(self, user_list: list[User]) -> None:
        with open(self.file_name, "w", encoding="utf-8") as file:
            for user in user_list:
                file.write(f"{user.userid}|{user.username}\n")

db = DBFile(config.USERS_DB_FILE)

