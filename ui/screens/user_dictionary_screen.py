from factories.dictionary_screen_renderer_factory import DictionaryWordRowRendererFactory
from ui.gui import add_col_label
from ui.popups.input_words_popup import InputEnglishWordPopup
from ui.renderers.user_dictionary_renderers import IDictionaryWordRowRenderer
from ui.screens.base_screen import BaseScreen


class UserDictionaryScreen(BaseScreen):
    """Экран словаря"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer: IDictionaryWordRowRenderer | None = None

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
        lang_code = self.state.get_language().lang_code
        self.renderer = DictionaryWordRowRendererFactory.create(lang_code)
        self.show_words()

    def show_words(self):
        """Показывает слова в таблице"""
        container = self.ids.words_container
        container.clear_widgets()

        if not self.state.get_dictionary():
            return

        words = self.state.get_dictionary().get_words()

        # ✅ Установим нужное количество колонок
        container.cols = self.renderer.get_column_count()

        self.renderer.render_headers(container)
        for word in words:
            self.renderer.render_word_row(container, word)
