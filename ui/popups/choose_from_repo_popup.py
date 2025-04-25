from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from factories.input_word_popup_factory import InputWordPopupFactory
from models.language import Language
from models.word import IBasicWord
from typing import Callable

from repositories.word_repo import WordRepository


class ChooseFromRepoPopup(Popup):
    def __init__(self,
                 words: list[IBasicWord],
                 language: Language,
                 word_repo: WordRepository,
                 on_words_selected: Callable = None,
                 on_add_new: Callable=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.language = language
        self.word_repo = word_repo
        self.all_words = words
        self.filtered_words = words
        self.on_words_selected = on_words_selected
        self.on_add_new = on_add_new
        self.checkboxes: list[tuple[CheckBox, IBasicWord]] = []
        self.update_word_list()

    def apply_filter(self):
        #query = self.filter_text.lower().strip()
        query = self.ids.filter_input.text.lower().strip()
        print(f"Filter query: {query}")
        self.filtered_words = [
            w for w in self.all_words if query in w.term.lower() or query in w.translation.lower()
        ]
        print(f"Filtered words: {self.filtered_words}")
        self.update_word_list()

    def update_word_list(self):
        container = self.ids.word_container
        container.clear_widgets()
        for word in self.filtered_words:
            container.add_widget(self.create_word_row(word))

    def create_word_row(self, word: IBasicWord):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label

        row = BoxLayout(orientation="horizontal", size_hint_y=None, height=30, spacing=10)
        checkbox = CheckBox()
        self.checkboxes.append((checkbox, word))  # сохраняем связь

        row.add_widget(checkbox)
        row.add_widget(Label(text=word.term, size_hint_x=0.3))
        row.add_widget(Label(text=word.translation, size_hint_x=0.4))
        return row

    def confirm_selection(self):
        # получить слова по чекбоксам
        selected_words = [word for checkbox, word in self.checkboxes if checkbox.active]
        if self.on_words_selected:
            self.on_words_selected(selected_words)
        self.dismiss()

    def add_new_word(self):
        lang_code = self.language.lang_code

        def save_word(term, translation, *args, **kwargs):
            self.word_repo.add_word(term, translation, *args, **kwargs)
            self.all_words.append(self.word_repo.find_word(term, translation))
            if self.on_add_new:
                self.on_add_new(self.word_repo.find_word(term, translation))
            self.update_word_list()

        popup = InputWordPopupFactory.create(lang_code, on_input_finished=save_word)
        popup.open()
