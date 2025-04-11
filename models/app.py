from models.user import User
from models.language import Language
from storage.user_repo import UserRepository

class AppState:
    def __init__(self):
        self.__user_repo = UserRepository()
        self.__user: User | None = None
        self.__language: Language | None = None

    def set_user_repo(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    def set_user(self, user: User):
        self.__user = user

    def set_language(self, language: Language):
        self.__language = language

    def get_user_repo(self) -> UserRepository:
        return self.__user_repo

    def get_user(self) -> User:
        return self.__user

    def get_language(self) -> Language:
        return self.__language