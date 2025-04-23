from datetime import datetime
from pathlib import Path

from models.user_dictionary import UserDictionary
from models.user_word import IBasicUserWord, BasicUserWord
from models.language import Language
from models.user import User
from repositories.word_repo import WordRepository
from storage.interfaces import IDictionaryStorage


class DictionaryFileStorage(IDictionaryStorage):
    def __init__(self, dictionary_data: dict[str, str]):
        self.__dictionary_data = dictionary_data

    def __get_dictionary_file_name(self, user: User, language: Language) -> str:
        file_path = (f"{self.__dictionary_data['DIRECTORY']}"
                     + f"{self.__dictionary_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def load_dictionary(self, user: User, language: Language, word_repo: WordRepository) -> UserDictionary:
        dictionary = UserDictionary(user, language, word_repo)
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        words: list[IBasicUserWord] = []
        try:
            with open(dictionary_file_name, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    term, translation, added_at = (parts + [""] * 3)[:3]
                    if added_at:
                        added_at = datetime.fromisoformat(added_at)
                    else:
                        added_at = datetime.now()
                    word = word_repo.find_word(term, translation)

                    words.append(BasicUserWord(word, added_at))
        except FileNotFoundError:
            print(f"Файл {dictionary_file_name} не найден. Будет создан при сохранении.")
        dictionary.set_words(words)
        return dictionary

    def save_dictionary(self, dictionary: UserDictionary) -> None:
        user = dictionary.get_user()
        language = dictionary.get_language()
        dictionary_file_name = self.__get_dictionary_file_name(user, language)
        with open(dictionary_file_name, "w", encoding="utf-8") as file:
            for word in dictionary.get_words():
                file.write(f"{word.word.term}|{word.word.translation}|{word.get_added_at()}\n")
