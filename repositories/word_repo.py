from factories.word_factory import WordFactory
from models.language import Language
from models.word import IBasicWord
from storage.interfaces import IWordStorage

class WordRepository:
    def __init__(self, storage: IWordStorage):
        self.language: Language | None = None
        self._storage: IWordStorage = storage
        self._words: list[IBasicWord] = []

    def add_word(self, term, translation, *args, **kwargs) -> None:
        # Проверяем, есть ли уже такое сочетание слово + перевод
        if self.find_word(term, translation):
            return  # Не добавляем дубликат
        word = WordFactory.create_word(self.language, term, translation, *args,
                                       **kwargs)
        self._words.append(word)

    def find_word(self, term, translation) -> IBasicWord | None:
        for w in self._words:
            if w.term == term and w.translation == translation:
                return w
        return None

    def get_words(self) -> list[IBasicWord]:
        return self._words