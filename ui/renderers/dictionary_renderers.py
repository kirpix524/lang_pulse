from abc import ABC, abstractmethod

from kivy.uix.label import Label

from models.word import IBasicWord, EnglishWord
from ui.types import SupportsAddWidget


class IDictionaryWordRowRenderer(ABC):
    @abstractmethod
    def render_headers(self, container: SupportsAddWidget):
        pass

    @abstractmethod
    def render_word_row(self, container: SupportsAddWidget, user_word: IBasicWord):
        pass

    @abstractmethod
    def get_column_count(self) -> int: pass

class BasicDictionaryWordRowRenderer(IDictionaryWordRowRenderer):
    def render_headers(self, container):
        headers = ["Слово", "Перевод"]
        for title in headers:
            container.add_widget(Label(
                text=title,
                bold=True,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=30,
                size_hint_x=None,
                width=150
            ))

    def render_word_row(self, container, word):
        container.add_widget(Label(
            text=word.term,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))
        container.add_widget(Label(
            text=word.translation,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))

    def get_column_count(self) -> int:
        return 2

class EnglishDictionaryWordRowRenderer(BasicDictionaryWordRowRenderer):
    def render_headers(self, container):
        headers = ["Слово", "Транскрипция", "Перевод"]
        for title in headers:
            container.add_widget(Label(
                text=title,
                bold=True,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=30,
                size_hint_x=None,
                width=150
            ))

    def render_word_row(self, container, word: EnglishWord):
        container.add_widget(Label(
            text=word.term,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))
        container.add_widget(Label(
            text=f"[{word.get_transcription()}]",
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))
        container.add_widget(Label(
            text=word.translation,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))

    def get_column_count(self) -> int:
        return 3