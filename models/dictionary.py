from factories.word_factory import WordFactory
from models.language import Language
from models.user import User
from models.stats import StatsRow
from datetime import datetime
from models.user_word import IBasicUserWord


class Dictionary:
    def __init__(self, user: User, language: Language):
        self.__user = user
        self.__language = language
        self.__words: list[IBasicUserWord] = []

    def set_words(self, words: list[IBasicUserWord]) -> None:
        self.__words = words

    def get_user(self) -> User:
        return self.__user

    def get_language(self) -> Language:
        return self.__language

    def get_words(self) -> list[IBasicUserWord]:
        return self.__words

    def find_word(self, word, translation) -> IBasicUserWord | None:
        for w in self.__words:
            if w.word == word and w.translation == translation:
                return w
        return None

    def add_word(self, word, translation, *args, **kwargs) -> None:
        # Проверяем, есть ли уже такое сочетание слово + перевод
        if self.find_word(word, translation):
            return # Не добавляем дубликат
        word = WordFactory.create_word(self.__language.lang_code, word, translation, added_at=datetime.now(), *args, **kwargs)
        self.__words.append(word)

    def update_training_stats(self, stats: list[StatsRow]) -> None:
        for stat in stats:
            word = self.find_word(str(stat.word), str(stat.translation))
            if not word:
                continue
            word.add_stat(stat)

    def get_words_not_in_list(self, words: list[IBasicUserWord]) -> list[IBasicUserWord]:
        return [w for w in self.__words if w.word not in words]