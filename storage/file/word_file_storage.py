from factories.word_factory import WordFactory
from models.language import Language
from pathlib import Path

from models.user_word import IBasicUserWord
from models.word import IBasicWord, EnglishWord
from storage.interfaces import IWordStorage


class WordFileStorage(IWordStorage):
    def __init__(self, words_data: dict[str, str]):
        self.__words_data = words_data

    def __get_word_repo_file_name(self, language: Language) -> str:
        file_path = (f"{self.__words_data['DIRECTORY']}"
                     + f"{self.__words_data['FILE_NAME_PREFIX']}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def load_word_list(self, language: Language) -> list[IBasicWord]:
        word_repo_file_name = self.__get_word_repo_file_name(language)
        words: list[IBasicWord] = []
        try:
            with open(word_repo_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    word = WordFactory.from_line(language, line)
                    words.append(word)
        except FileNotFoundError:
            print(f"Файл {word_repo_file_name} не найден. Будет создан при сохранении.")
        return words

    def save_word_list(self, words: list[IBasicWord], language: Language) -> None:
        file_path = self.__get_word_repo_file_name(language)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for word in words:
                    f.write(word.to_line() + "\n")
        except Exception as e:
            print(f"Ошибка при сохранении слов в {file_path}: {e}")

    def save_word(self, word: IBasicWord, language: Language) -> None:
        file_path = self.__get_word_repo_file_name(language)
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(word.to_line() + "\n")
        except Exception as e:
            print(f"Ошибка при добавлении слова в {file_path}: {e}")

