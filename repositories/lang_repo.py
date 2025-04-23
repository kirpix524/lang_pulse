from models.language import Language
from storage.interfaces import ILanguageStorage


class LanguageRepository:
    def __init__(self, storage: ILanguageStorage):
        self.__storage = storage
        self.languages: list[Language] = self.__storage.load_language_list()

    def __get_new_language_id(self):
        return max((lang.lang_id for lang in self.languages), default=0) + 1

    def add_language(self, lang_name: str, lang_code:str) -> None:
        self.languages.append(Language(self.__get_new_language_id(), lang_name, lang_code))
        self.__storage.save_language_list(self.languages)

    def language_exists(self, lang_name: str) -> bool:
        return any(language.lang_name == lang_name for language in self.languages)

    def get_language_names(self) -> list[str]:
        return [lang.lang_name for lang in self.languages]

    def get_language_by_name(self, lang_name) -> Language:
        return next((lang for lang in self.languages if lang.lang_name==lang_name), None)