from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
import storage.config as config
from storage.user_repo import UserRepository

# Экран выбора пользователя
class LoginScreen(Screen):
    def __init__(self, user_repo, **kwargs):
        super().__init__(**kwargs)
        self.user_repo = user_repo

    def on_enter(self):
        """Вызывается при входе на экран"""
        usernames = self.user_repo.get_usernames()
        self.ids.spinner.values = usernames

    def login(self):
        username = self.ids.spinner.text
        if self.user_repo.user_exists(username):
            self.manager.current_user = username
            self.manager.current = 'main_menu'

    def goto_register(self):
        self.manager.current = 'register'

# Экран регистрации
class RegisterScreen(Screen):
    def __init__(self, user_repo, **kwargs):
        super().__init__(**kwargs)
        self.user_repo = user_repo

    def register(self):
        username = self.ids.username_input.text.strip()
        if username and not self.user_repo.user_exists(username):
            self.user_repo.add_user(username)
            self.manager.current_user = username
            self.manager.get_screen('login').ids.spinner.values = self.user_repo.get_usernames()
            self.manager.current = 'main_menu'

# Главное меню
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Менеджер экранов
class LangPulseApp(App):
    def build(self):
        self.user_repo = UserRepository()
        self.sm = ScreenManager()
        self.sm.current_user = None
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}main_menu.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}login.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}register.kv")

        self.sm.add_widget(LoginScreen(name='login', user_repo=self.user_repo))
        self.sm.add_widget(RegisterScreen(name='register', user_repo=self.user_repo))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))

        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm
