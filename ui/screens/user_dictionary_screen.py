from ui.gui import add_col_label
from ui.popups.input_words_popup import InputEnglishWordPopup
from ui.screens.base_screen import BaseScreen


class UserDictionaryScreen(BaseScreen):
    """Экран словаря"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_word(self):
        """Обрабатывает нажатие кнопки "Добавить слово" """
        def save_word(term, translation, transcription):
            self.state.get_dictionary().add_word(term, translation, transcription=transcription)
            self.ctx.user_dictionary_storage.save_dictionary(self.state.get_dictionary())
            self.show_words()
        popup = InputEnglishWordPopup(on_input_finished=save_word)
        popup.open()

    def on_pre_enter(self):
        super().on_pre_enter()
        self.show_words()

    def show_words(self):
        """Показывает слова в таблице"""
        container = self.ids.words_container
        container.clear_widgets()

        if not self.state.get_dictionary():
            return

        words = self.state.get_dictionary().get_words()

        # Заголовки таблицы
        headers = ["Слово", "Транскрипция", "Перевод", "Добавлено", "Последнее повторение"]
        for title in headers:
            add_col_label(container, title)

        for word in words:
            add_col_label(container, word.word.term)
            add_col_label(container, f"[{word.word.get_transcription()}]")
            add_col_label(container, word.word.translation)
            add_col_label(container, word.get_added_at_str())
            add_col_label(container, word.get_last_repeated_at_str())
