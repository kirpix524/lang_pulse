from models.language import Language
from storage.db import db
class LanguageRepository:
    def __init__(self):
        self.languages: list[Language] = db.load_language_list()

    def __get_new_language_id(self):
        return len(self.languages)

    def add_language(self, lang_name: str, lang_code:str) -> None:
        self.languages.append(Language(self.__get_new_language_id(), lang_name, lang_code))
        db.save_language_list(self.languages)

    def language_exists(self, lang_name: str) -> bool:
        return any(language.lang_name == lang_name for language in self.languages)

    def get_language_names(self) -> list[str]:
        return [lang.lang_name for lang in self.languages]

    def get_language_by_name(self, lang_name) -> Language:
        return next((lang for lang in self.languages if lang.lang_name==lang_name), None)