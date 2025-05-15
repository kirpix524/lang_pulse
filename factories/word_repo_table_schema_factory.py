from typing import Type

from models.language import Language
from storage.sqlite.schema.word_repo_schema import IWordRepoTableSchema

class WordRepoTableSchemaFactory:
    _registry: dict[str, Type[IWordRepoTableSchema]] = {}

    @classmethod
    def register(cls, lang_code: str, schema_class: Type[IWordRepoTableSchema]) -> None:
        cls._registry[lang_code.lower()] = schema_class

    @classmethod
    def create_schema(cls, language: Language, table_prefix: str, *args, **kwargs) -> IWordRepoTableSchema:
        table_schema_class = cls._registry.get(language.lang_code.lower())
        if not table_schema_class:
            raise ValueError(f"No table schema registered for language: {language.lang_name}")
        return table_schema_class(language, table_prefix, *args, **kwargs)