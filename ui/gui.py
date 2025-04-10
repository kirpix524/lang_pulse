from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import storage.config as config
from storage.user_repo import UserRepository
from models.user import User

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
            self.manager.current_user = self.user_repo.get_user_by_name(username)
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
            self.manager.current_user = self.user_repo.get_user_by_name(username)
            self.manager.get_screen('login').ids.spinner.values = self.user_repo.get_usernames()
            self.manager.current = 'main_menu'

# Главное меню
class MainMenuScreen(Screen):
    current_user_name = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        self.current_user_name = self.manager.current_user.username or ''

    def show_dictionary(self):
        self.manager.get_screen('dictionary').set_user(self.manager.current_user)
        self.manager.current = 'dictionary'

# Экран словаря
class DictionaryScreen(Screen):
    current_user_name = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__user = None

    def on_pre_enter(self):
        self.current_user_name = self.get_user_name()

    def set_user(self, user: User):
        self.__user = user

    def get_user_name(self) -> str:
        if self.__user:
            return self.__user.username
        else:
            return ""


# Менеджер экранов
class LangPulseApp(App):
    def build(self):
        self.user_repo = UserRepository()
        self.sm = ScreenManager()
        self.sm.current_user = None
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}main_menu.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}login.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}register.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}dictionary.kv")

        self.sm.add_widget(LoginScreen(name='login', user_repo=self.user_repo))
        self.sm.add_widget(RegisterScreen(name='register', user_repo=self.user_repo))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(DictionaryScreen(name='dictionary'))

        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm
