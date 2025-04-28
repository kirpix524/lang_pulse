from models.language import Language
from models.user import User
from models.stats import StatsRow
from datetime import datetime
from models.user_word import IBasicUserWord, BasicUserWord
from models.word import IBasicWord
from repositories.word_repo import WordRepository


class UserDictionary:
    def __init__(self, user: User, language: Language, word_repo: WordRepository):
        self.__user = user
        self.__language = language
        self.__word_repo = word_repo
        self.__words: list[IBasicUserWord] = []

    def set_words(self, words: list[IBasicUserWord]) -> None:
        self.__words = words

    def get_user(self) -> User:
        return self.__user

    def get_language(self) -> Language:
        return self.__language

    def get_words(self) -> list[IBasicUserWord]:
        return self.__words

    def find_word(self, term, translation) -> IBasicUserWord | None:
        for w in self.__words:
            if w.word.term == term and w.word.translation == translation:
                return w
        return None

    def _find_word_by_object(self, word: IBasicWord) -> IBasicUserWord | None:
        for w in self.__words:
            if w.word == word:
                return w
        return None

    def add_word(self, word: IBasicWord, added_at: datetime=None, *args, **kwargs) -> None:
        # Проверяем, есть ли уже такое сочетание слово + перевод
        if self._find_word_by_object(word):
            return # Не добавляем дубликат
        if not added_at:
            added_at = datetime.now()
        user_word = BasicUserWord(word, added_at)
        self.__words.append(user_word)

    def update_training_stats(self, stats: list[StatsRow]) -> None:
        for stat in stats:
            word = self.find_word(str(stat.term), str(stat.translation))
            if not word:
                continue
            word.add_stat(stat)

    def get_words_not_in_list(self, words: list[IBasicUserWord]) -> list[IBasicUserWord]:
        word_keys = {(w.word.term, w.word.translation) for w in words}
        return [w for w in self.__words if (w.word.term, w.word.translation) not in word_keys]