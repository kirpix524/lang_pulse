from storage.db import db
from models.user import User
# Временная заглушка вместо настоящего хранилища пользователей
class UserRepository:
    def __init__(self):
        self.users: list[User] = db.load_user_list()

    def __get_new_user_id(self):
        return len(self.users)

    def add_user(self, username):
        user = User(username, self.__get_new_user_id())
        self.users.append(user)
        db.save_user_list(self.users)

    def get_usernames(self) -> list[str]:
        return [user.username for user in self.users]

    def user_exists(self, username: str) -> bool:
        return any(user.username == username for user in self.users)