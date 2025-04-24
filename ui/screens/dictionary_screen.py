from factories.dictionary_screen_renderer_factory import DictionaryWordRowRendererFactory
from factories.input_word_popup_factory import InputWordPopupFactory
from ui.renderers.dictionary_renderers import IDictionaryWordRowRenderer
from ui.screens.base_screen import BaseScreen


class DictionaryScreen(BaseScreen):
    """Экран словаря"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer: IDictionaryWordRowRenderer | None = None

    def add_word(self):
        """Обрабатывает нажатие кнопки "Добавить слово" """
        lang_code = self.state.get_language().lang_code
        def save_word(term, translation, *args, **kwargs):
            self.ctx.get_word_repo().add_word(term, translation, *args, **kwargs)
            self.show_words()
        popup = InputWordPopupFactory.create(lang_code, on_input_finished=save_word)
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

        if not self.ctx.get_word_repo():
            return

        words = self.ctx.get_word_repo().get_words()

        words.sort(key=lambda w: w.term)

        # ✅ Установим нужное количество колонок
        container.cols = self.renderer.get_column_count()

        self.renderer.render_headers(container)
        for word in words:
            self.renderer.render_word_row(container, word)