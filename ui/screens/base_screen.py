from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from app.state import AppState
from app.context import AppContext


class BaseScreen(Screen):
    current_user_name = StringProperty('')
    current_language_name = StringProperty('')

    def on_pre_enter(self):
        if self.state.get_user():
            self.current_user_name = self.state.get_user().username or ''
        if self.state.get_language():
            self.current_language_name = self.state.get_language().lang_name or ''

    def goto_screen(self, screen_name):
        self.manager.current = screen_name

    @property
    def state(self) -> AppState:
        return self.manager.state

    @property
    def ctx(self) -> AppContext:
        return self.manager.ctx
