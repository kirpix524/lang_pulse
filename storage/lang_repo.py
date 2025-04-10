from storage.db import db
class LanguageRepository:
    def __init__(self):
        self.languages = db.load_language_list()

    def __get_new_language_id(self):
        return len(self.languages)

    def add_language(self, lang_name: str, lang_code:str) -> None:
        self.languages.append((self.__get_new_language_id(), lang_name, lang_code))
        db.save_language_list(self.languages)

