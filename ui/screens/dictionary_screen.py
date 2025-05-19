from factories.dictionary_screen_renderer_factory import DictionaryWordRowRendererFactory
from factories.input_word_popup_factory import InputWordPopupFactory
from factories.word_factory import WordFactory
from ui.popups.file_selection_popup import FileSelectionPopup
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

    def add_words_from_file(self) -> None:
        popup = FileSelectionPopup(on_selection_finished=self._process_file)
        popup.open()

    def _process_file(self, filepath: str) -> None:
        repo = self.ctx.get_word_repo()
        existing = {(w.term, w.translation) for w in repo.get_words()}

        if not filepath.lower().endswith('.txt'):
            return

        with open(filepath, encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                word = WordFactory.from_line(self.state.get_language(), line)
                term = word.term
                translation = word.translation
                if (term, translation) not in existing:
                    repo.add_word_object(word)
                    existing.add((term, translation))

        self.show_words()

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