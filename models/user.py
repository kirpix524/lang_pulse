
class User:
    def __init__(self, username: str, userid: int):
        self._username = username
        self._userid = userid

    @property
    def username(self) -> str:
        return self._username if self._username else ''

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def userid(self) -> int:
        return self._userid
