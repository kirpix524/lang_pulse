from models.language import Language
from storage.interfaces import ILanguageStorage


class LanguageFileStorage(ILanguageStorage):
    def __init__(self, file_names: dict[str, str]):
        self.__file_names = file_names

    def load_language_list(self) -> list[Language]:
        languages: list[Language] = []
        try:
            with open(self.__file_names["LANGUAGES"], "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    language_id, language_name, language_code = line.split("|", 2)
                    language = Language(int(language_id.strip()), language_name.strip(), language_code.strip())
                    languages.append(language)
        except FileNotFoundError:
            print(f"Файл {self.__file_names["LANGUAGES"]} не найден. Будет создан при сохранении.")

        return languages

    def save_language_list(self, language_list: list[Language]) -> None:
        with open(self.__file_names["LANGUAGES"], "w", encoding="utf-8") as file:
            for language in language_list:
                file.write(f"{language.lang_id}|{language.lang_name}|{language.lang_code}\n")

    def save_language(self, language: Language) -> None:
        languages = self.load_language_list()
        fl_found = False
        for l in languages:
            if l.lang_id == language.lang_id:
                fl_found = True
                break
        if not fl_found:
            languages.append(language)
        self.save_language_list(languages)

