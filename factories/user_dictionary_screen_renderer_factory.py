from ui.renderers.user_dictionary_renderers import IUserDictionaryWordRowRenderer, BasicUserDictionaryWordRowRenderer


class UserDictionaryWordRowRendererFactory:
    __registry: dict[str, type[IUserDictionaryWordRowRenderer]] = {}

    @classmethod
    def register(cls, lang_code: str, renderer_cls: type[IUserDictionaryWordRowRenderer]):
        cls.__registry[lang_code] = renderer_cls

    @classmethod
    def create(cls, lang_code: str) -> IUserDictionaryWordRowRenderer:
        renderer_cls = cls.__registry.get(lang_code, BasicUserDictionaryWordRowRenderer)
        return renderer_cls()
