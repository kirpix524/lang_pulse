from storage.interfaces import IUserStorage
from models.user import User

class UserRepository:
    def __init__(self, storage: IUserStorage):
        self._storage = storage
        self._users: list[User] = self._storage.load_user_list()

    def __get_new_user_id(self):
        return max((user.userid for user in self._users), default=0) + 1

    def add_user(self, username):
        user = User(username, self.__get_new_user_id())
        self._users.append(user)
        self._storage.save_user_list(self._users)

    def get_usernames(self) -> list[str]:
        return [user.username for user in self._users]

    def user_exists(self, username: str) -> bool:
        return any(user.username == username for user in self._users)

    def get_user_by_name(self, username: str) -> User:
        return next((user for user in self._users if user.username == username), None)