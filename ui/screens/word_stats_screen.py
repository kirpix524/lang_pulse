from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from models.stats import StatsRow
from models.user_word import IBasicUserWord
from ui.popups.choose_words_popup import ChooseWordsPopup
from ui.screens.base_screen import BaseScreen


class WordStatsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__words_for_stats: list[IBasicUserWord] = []
        self.__stats_user = None
        self.__stats_language = None


    def on_pre_enter(self):
        super().on_pre_enter()
        if self.__stats_user != self.state.get_user() or self.__stats_language != self.state.get_language():
            self.__words_for_stats.clear()
            self.__stats_user = self.state.get_user()
            self.__stats_language = self.state.get_language()
        self.show_stats()

    def add_words_for_stats(self):
        dictionary = self.state.get_dictionary()
        if not dictionary:
            return

        available_words = [w for w in dictionary.get_words() if w not in self.__words_for_stats]

        def on_added(words):
            self.__words_for_stats.extend(words)
            self.show_stats()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_added)
        popup.open()

    def remove_words_for_stats(self):
        if not self.__words_for_stats:
            return

        def on_removed(words):
            for w in words:
                if w in self.__words_for_stats:
                    self.__words_for_stats.remove(w)
            self.show_stats()

        popup = ChooseWordsPopup(words=self.__words_for_stats, on_words_selected=on_removed)
        popup.open()

    def show_stats(self):
        container = self.ids.stats_container
        container.clear_widgets()

        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=5)
        header.add_widget(Label(text="Результат", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100))
        header.add_widget(Label(text="Время", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100))
        header.add_widget(Label(text="Дата", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=140))
        header.add_widget(Label(text="Направление", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=80))
        container.add_widget(header)

        for word in self.__words_for_stats:
            stats = word.get_stats()
            container.add_widget(self.create_word_row(word))
            if not stats:
                continue

            for stat in stats:
                container.add_widget(self.create_stat_row(stat))

    def create_word_row(self, word: IBasicUserWord):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=5)

        row.add_widget(Label(text=word.word.term, font_size='18sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text=word.word.translation, font_size='18sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text='', size_hint_x=None, width=140, size_hint_y=None, height=30))
        row.add_widget(Label(text='', size_hint_x=None, width=80, size_hint_y=None, height=30))
        return row

    def create_stat_row(self, stat: StatsRow):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=5)

        row.add_widget(Label(text="Правильно" if stat.success else "Неправильно", color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text=f"{stat.recall_time}s" if stat.recall_time else "-", color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text=stat.get_timestamp_str(), color=(0, 0, 0, 1), size_hint_x=None, width=140, size_hint_y=None, height=30))
        row.add_widget(Label(text=stat.get_direction_name(), color=(0, 0, 0, 1), size_hint_x=None, width=80))

        return row
