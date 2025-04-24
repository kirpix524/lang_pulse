from ui.renderers.user_dictionary_renderers import IDictionaryWordRowRenderer, BasicDictionaryWordRowRenderer


class DictionaryWordRowRendererFactory:
    __registry: dict[str, type[IDictionaryWordRowRenderer]] = {}

    @classmethod
    def register(cls, lang_code: str, renderer_cls: type[IDictionaryWordRowRenderer]):
        cls.__registry[lang_code] = renderer_cls

    @classmethod
    def create(cls, lang_code: str) -> IDictionaryWordRowRenderer:
        renderer_cls = cls.__registry.get(lang_code, BasicDictionaryWordRowRenderer)
        return renderer_cls()
