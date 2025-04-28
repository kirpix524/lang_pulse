class Language:
    def __init__(self, lang_id, lang_name, lang_code):
        self._lang_name = lang_name
        self._lang_id = lang_id
        self._lang_code = lang_code

    @property
    def lang_id(self) -> int:
        return self._lang_id

    @property
    def lang_name(self) -> str:
        return self._lang_name

    @property
    def lang_code(self) -> str:
        return self._lang_code
