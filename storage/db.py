import json
import os

from docutils.parsers.rst.directives.misc import Class

from models.user import User
from models.word import Word

class DataBase:
    def __init__(self):
        pass

    def save_user(self, user: User):
        pass

    def save_user_list(self, user_list: []):
        pass

    def save_word(self, word: Word):
        pass

    def load_user_list(self):
        pass

    def load_word_list(self, user:User):
        pass

    def load_user(self, user:User):
        pass

class DBFile(DataBase):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def load_user_list(self):
        users = []
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    user_id, username = line.split("|", 1)
                    users[username] = User(user_id.strip(), username.strip())
        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден. Будет создан при сохранении.")

    def save_user_list(self, user_list):
        with open(self.file_name, "w", encoding="utf-8") as file:
            for user in user_list.values():
                file.write(f"{user.id}|{user.username}\n")


