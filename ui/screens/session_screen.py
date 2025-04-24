from ui.gui import add_col_label, show_message
from ui.popups.choose_words_popup import ChooseWordsPopup
from ui.popups.direction_select_popup import DirectionSelectPopup
from ui.screens.base_screen import BaseScreen


class SessionScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.show_words()

    def show_words(self):
        self.ids.words_container.clear_widgets()
        session = self.state.get_session()
        if not session:
            return
        for word in session.get_words():
            add_col_label(self.ids.words_container, word.word.term)

    def start_training(self):
        interval_text = self.ids.interval_input.text.strip()

        if not interval_text:
            show_message("Ошибка", "Введите интервал в секундах")
            return

        interval = float(interval_text)
        session = self.state.get_session()

        if not session or len(session.get_words())<5:
            show_message("Ошибка", "Добавьте не менее 5 слов в тренировку")
            return



        def on_direction_chosen(direction):
            session.add_new_training(direction, interval)
            self.goto_screen('session_training')

        popup = DirectionSelectPopup(on_selected=on_direction_chosen)
        popup.open()

    def add_words_to_session(self):
        # Реализация добавления слова в тренировку
        session = self.state.get_session()
        if not session.can_be_changed():
            show_message("Ошибка", "Эта тренировка уже запускалась и ее нельзя изменять")
            return
        dictionary = self.state.get_dictionary()

        if not dictionary or not session:
            show_message("Ошибка", "Словарь или тренировка не найдены")

        available_words = dictionary.get_words_not_in_list(session.get_words())

        def on_added(words):
            session.add_words(words)
            self.ctx.session_storage.save_all_sessions(self.state.get_user(), self.state.get_language(), self.ctx.get_session_repo().get_sessions())
            self.show_words()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_added)
        popup.open()

    def remove_words_from_session(self):
        # Реализация удаления слова из тренировки
        session = self.state.get_session()
        if not session.can_be_changed():
            show_message("Ошибка", "Эта тренировка уже запускалась и ее нельзя изменять")
            return

        if not session:
            show_message("Ошибка", "Словарь или тренировка не найдены")

        available_words = session.get_words()

        def on_deleted(words):
            session.del_words(words)
            self.ctx.session_storage.save_all_sessions(self.state.get_user(), self.state.get_language(), self.ctx.get_session_repo().get_sessions())
            self.show_words()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_deleted)
        popup.open()
