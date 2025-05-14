from abc import abstractmethod, ABC

class IBasicWord(ABC):
    _term: str
    _translation: str

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def from_line(cls, line: str) -> "IBasicWord":
        pass

    @abstractmethod
    def to_line(self) -> str:
        pass

    @property
    @abstractmethod
    def term(self) -> str:
        pass

    @term.setter
    @abstractmethod
    def term(self, value: str):
        pass


    @property
    @abstractmethod
    def translation(self) -> str:
        pass

    @translation.setter
    @abstractmethod
    def translation(self, value: str):
        pass

class BasicWord(IBasicWord):
    def __init__(self, term, translation):
        super().__init__()
        self._term = term
        self._translation = translation

    @classmethod
    def from_line(cls, line: str) -> "BasicWord":
        parts = line.strip().split("|")
        word, translation = (parts + [""] * 2)[:2]
        return cls(word, translation)

    def to_line(self) -> str:
        return f"{self.term}|{self.translation}"

    @property
    def term(self) -> str:
        return self._term

    @term.setter
    def term(self, value: str):
        self._term = value

    @property
    def translation(self) -> str:
        return self._translation

    @translation.setter
    def translation(self, value: str):
        self._translation = value


class EnglishWord(BasicWord):
    _transcription: str | None
    def __init__(self, term, translation, transcription=None):
        super().__init__(term, translation)
        self._transcription = transcription

    @classmethod
    def from_line(cls, line: str) -> "EnglishWord":
        parts = line.strip().split("|")
        term, translation, transcription = (parts + [""] * 3)[:3]
        return cls(term, translation, transcription)

    def to_line(self) -> str:
        return f"{self.term}|{self.translation}|{self.transcription}"

    @property
    def transcription(self) -> str:
        return self._transcription if self._transcription else ''

    @transcription.setter
    def transcription(self, value: str):
        self._transcription = value