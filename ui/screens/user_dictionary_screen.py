from factories.user_dictionary_screen_renderer_factory import UserDictionaryWordRowRendererFactory
from factories.input_word_popup_factory import InputWordPopupFactory
from ui.popups.choose_from_repo_popup import ChooseFromRepoPopup
from ui.renderers.user_dictionary_renderers import IUserDictionaryWordRowRenderer
from ui.screens.base_screen import BaseScreen


class UserDictionaryScreen(BaseScreen):
    """Экран словаря"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer: IUserDictionaryWordRowRenderer | None = None

    def add_word(self):
        """Обрабатывает нажатие кнопки "Добавить слово" """
        all_words = self.ctx.get_word_repo().get_words()
        user_words = self.state.get_dictionary().get_words()
        user_words_pairs = [(w.word.term, w.word.translation) for w in user_words]
        available_words = [w for w in all_words if (w.term, w.translation) not in user_words_pairs]

        def on_selected(words):
            for word in words:
                self.state.get_dictionary().add_word(word)
            self.ctx.user_dictionary_storage.save_dictionary(self.state.get_dictionary())
            self.show_words()

        def on_add_new(term):
            # показать попап для ввода перевода, затем сохранить в общий словарь и пользовательский
            pass

        popup = ChooseFromRepoPopup(
            available_words,
            self.state.get_language(),
            self.ctx.get_word_repo(),
            on_words_selected=on_selected,
            on_add_new=on_add_new
        )
        popup.open()

    def on_pre_enter(self):
        super().on_pre_enter()
        lang_code = self.state.get_language().lang_code
        self.renderer = UserDictionaryWordRowRendererFactory.create(lang_code)
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
