from abc import abstractmethod, ABC



class IBasicWord(ABC):
    term: str
    translation: str

    @classmethod
    @abstractmethod
    def from_line(cls, line: str) -> "IBasicWord":
        pass

    @abstractmethod
    def to_line(self) -> str:
        pass

class BasicWord(IBasicWord):
    def __init__(self, word, translation):
        self.term = word
        self.translation = translation

    @classmethod
    def from_line(cls, line: str) -> "BasicWord":
        parts = line.strip().split("|")
        word, translation = (parts + [""] * 2)[:2]
        return cls(word, translation)

    def to_line(self) -> str:
        return f"{self.term}|{self.translation}"

class EnglishWord(BasicWord):
    _translation: str | None
    def __init__(self, word, translation, transcription=None):
        super().__init__(word, translation)
        self._transcription = transcription

    @classmethod
    def from_line(cls, line: str) -> "EnglishWord":
        parts = line.strip().split("|")
        word, translation, transcription = (parts + [""] * 3)[:3]
        return cls(word, translation, transcription)

    def to_line(self) -> str:
        return f"{self.term}|{self.translation}|{self.get_transcription()}"

    def get_transcription(self) -> str:
        return self._transcription if self._transcription else ''