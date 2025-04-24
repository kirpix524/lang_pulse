from ui.gui import show_message
from ui.screens.base_screen import BaseScreen


class RegisterScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register(self):
        username = self.ids.username_input.text.strip()
        if username:
            if not self.ctx.get_user_repo().user_exists(username):
                self.ctx.get_user_repo().add_user(username)
                self.state.set_user(self.ctx.get_user_repo().get_user_by_name(username))
                self.goto_screen('login')
            else:
                show_message("Ошибка","Такое имя пользователя уже есть")
        else:
            show_message("Ошибка","Введите имя пользователя")
