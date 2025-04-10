from models.language import Language


class User:
    def __init__(self, username: str, userid: int):
        self.username = username
        self.userid = userid
        self.language = None

    def set_language(self, language: Language) -> None:
        self.language = language

    def get_language_name(self) -> str:
        return self.language.name or ''
