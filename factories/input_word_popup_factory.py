from kivy.uix.popup import Popup


class InputWordPopupFactory:
    _registry: dict[str, type] = {}

    @classmethod
    def register(cls, lang_code: str, popup_cls: type):
        cls._registry[lang_code] = popup_cls

    @classmethod
    def create(cls, lang_code: str, on_input_finished) -> Popup:
        popup_cls = cls._registry.get(lang_code)
        if not popup_cls:
            raise ValueError(f"No input popup registered for language: {lang_code}")
        return popup_cls(on_input_finished=on_input_finished)