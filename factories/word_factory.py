from models.language import Language
from models.word import IBasicWord


class WordFactory:
    _registry: dict[str, type[IBasicWord]] = {}

    @classmethod
    def register(cls, lang_code: str, word_class):
        cls._registry[lang_code.lower()] = word_class

    @classmethod
    def create_word(cls, language: Language, *args, **kwargs) -> IBasicWord:
        word_class = cls._registry.get(language.lang_code.lower())
        if not word_class:
            raise ValueError(f"No Word class registered for language: {language}")
        return word_class(*args, **kwargs)

    @classmethod
    def from_line(cls, language: Language, line: str) -> IBasicWord:
        word_class = cls._registry.get(language.lang_code)
        if not word_class:
            raise ValueError(f"No word class registered for language: {language.lang_code}")
        return word_class.from_line(line)
