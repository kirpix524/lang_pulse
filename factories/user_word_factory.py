from typing import Type

from models.language import Language
from models.user_word import IBasicUserWord


class UserWordFactory:
    registry: dict[str, Type[IBasicUserWord]] = {}

    @classmethod
    def register(cls, lang_code: str, word_class):
        cls.registry[lang_code.lower()] = word_class

    @classmethod
    def create_word(cls, language: Language, *args, **kwargs) -> IBasicUserWord:
        word_class = cls.registry.get(language.lang_code.lower())
        if not word_class:
            raise ValueError(f"No Word class registered for language: {language.lang_name}")
        return word_class(*args, **kwargs)
