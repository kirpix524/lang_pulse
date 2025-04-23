from models.user import User
from storage.interfaces import IUserStorage


class UserFileStorage(IUserStorage):
    def __init__(self, file_names: dict[str, str]):
        self.__file_names = file_names

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
