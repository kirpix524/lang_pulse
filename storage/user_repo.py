from storage.db import IUserStorage
from models.user import User
# Временная заглушка вместо настоящего хранилища пользователей
class UserRepository:
    def __init__(self, storage: IUserStorage):
        self.__storage = storage
        self.users: list[User] = self.__storage.load_user_list()

    def __get_new_user_id(self):
        return len(self.users)

    def add_user(self, username):
        user = User(username, self.__get_new_user_id())
        self.users.append(user)
        self.__storage.save_user_list(self.users)

    def get_usernames(self) -> list[str]:
        return [user.username for user in self.users]

    def user_exists(self, username: str) -> bool:
        return any(user.username == username for user in self.users)

    def get_user_by_name(self, username: str) -> User:
        return next((user for user in self.users if user.username == username), None)