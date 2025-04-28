from abc import ABC, abstractmethod

from kivy.uix.label import Label

from models.user_word import IBasicUserWord, EnglishUserWord
from ui.types import SupportsAddWidget


class IUserDictionaryWordRowRenderer(ABC):
    @abstractmethod
    def render_headers(self, container: SupportsAddWidget):
        pass

    @abstractmethod
    def render_word_row(self, container: SupportsAddWidget, user_word: IBasicUserWord):
        pass

    @abstractmethod
    def get_column_count(self) -> int: pass

class BasicUserDictionaryWordRowRenderer(IUserDictionaryWordRowRenderer):
    def render_headers(self, container):
        headers = ["Слово", "Перевод", "Добавлено", "Последнее повторение"]
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

    def render_word_row(self, container, user_word):
        word = user_word.word

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
        container.add_widget(Label(
            text=user_word.get_added_at_str(),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))
        container.add_widget(Label(
            text=user_word.get_last_repeated_at_str(),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150
        ))

    def get_column_count(self) -> int:
        return 4

class EnglishUserDictionaryWordRowRenderer(BasicUserDictionaryWordRowRenderer):
    def render_headers(self, container):
        headers = ["Слово", "Транскрипция", "Перевод", "Добавлено", "Последнее повторение"]
        for title in headers:
            container.add_widget(Label(
                text=title,
                bold=True,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=30,
                size_hint_x=0.2
            ))

    def render_word_row(self, container, user_word: EnglishUserWord):
        word = user_word.word

        container.add_widget(Label(
            text=word.term,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=0.2
        ))
        container.add_widget(Label(
            text=f"[{word.transcription}]",
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=0.2
        ))
        container.add_widget(Label(
            text=word.translation,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=0.2
        ))
        container.add_widget(Label(
            text=user_word.get_added_at_str(),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=0.2
        ))
        container.add_widget(Label(
            text=user_word.get_last_repeated_at_str(),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30,
            size_hint_x=0.2
        ))

    def get_column_count(self) -> int:
        return 5