from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class ChooseWordsPopup(Popup):
    def __init__(self, words, on_words_selected, **kwargs):
        super().__init__(**kwargs)
        self.words = words
        self.on_words_selected = on_words_selected
        self.checkboxes = {}
        self.populate_word_list()

    def populate_word_list(self):
        grid = self.ids.words_grid
        grid.clear_widgets()

        # Заголовки
        grid.add_widget(Label(text='', bold=True))
        for header in ["Слово", "Транскрипция", "Перевод", "Добавлено", "Последнее повторение"]:
            grid.add_widget(Label(text=header, bold=True))

        for word in self.words:
            cb = CheckBox(size_hint=(None, None), size=(30, 30))
            self.checkboxes[word] = cb
            grid.add_widget(cb)

            grid.add_widget(Label(text=word.term, size_hint_x=None, width=150))
            grid.add_widget(Label(text=word.get_transcription(), size_hint_x=None, width=150))
            grid.add_widget(Label(text=word.translation, size_hint_x=None, width=150))
            grid.add_widget(Label(text=word.get_added_at_str(), size_hint_x=None, width=100))
            grid.add_widget(Label(text=word.get_last_repeated_at_str(), size_hint_x=None, width=100))

    def select_words(self):
        selected = [word for word, cb in self.checkboxes.items() if cb.active]
        self.on_words_selected(selected)
        self.dismiss()
