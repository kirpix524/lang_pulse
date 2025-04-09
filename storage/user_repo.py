# Временная заглушка вместо настоящего хранилища пользователей
class UserRepository:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        self.users[username] = {}

    def get_usernames(self):
        return list(self.users.keys())

    def user_exists(self, username):
        return username in self.users