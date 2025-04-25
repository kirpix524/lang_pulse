from ui.gui import show_message
from ui.screens.base_screen import BaseScreen


class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        """Вызывается при входе на экран"""
        self.ids.username_spinner.values = self.ctx.get_user_repo().get_usernames()
        self.ids.language_spinner.values = self.ctx.get_lang_repo().get_language_names()
        if self.state.get_user():
            self.ids.username_spinner.text = str(self.state.get_user().username)
        if self.state.get_language():
            self.ids.language_spinner.text = str(self.state.get_language().lang_name)

    def login(self):
        username = self.ids.username_spinner.text
        lang_name = self.ids.language_spinner.text
        if self.ctx.get_user_repo().user_exists(username):
            if self.ctx.get_lang_repo().get_language_by_name(lang_name):
                self.state.set_user(self.ctx.get_user_repo().get_user_by_name(username))
                self.state.set_language(self.ctx.get_lang_repo().get_language_by_name(lang_name))
                self.ctx.get_word_repo().set_language(self.state.get_language())

                self.state.set_dictionary(self.ctx.user_dictionary_storage.load_dictionary(self.state.get_user(), self.state.get_language(), self.ctx.get_word_repo()))
                self.ctx.stats_storage.load_training_stats_words(self.state.get_user(), self.state.get_language(), self.state.get_dictionary())
                self.ctx.get_session_repo().set_session_context(self.state.get_user(), self.state.get_language(), self.state.get_dictionary())
                self.goto_screen('main_menu')
            else:
                show_message("Ошибка",'Нужно выбрать язык')
        else:
            show_message("Ошибка",'Пользователь не выбран')
