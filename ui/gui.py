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
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.spinner = Spinner(text=config.LOGIN_SCREEN_CHOOSE_USER_TEXT, values=self.user_repo.get_usernames())
        self.login_button = Button(text=config.LOGIN_SCREEN_LOGIN_BUTTON_TEXT)
        self.register_button = Button(text=config.LOGIN_SCREEN_REGISTER_BUTTON_TEXT)

        self.layout.add_widget(self.spinner)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.register_button)

        self.login_button.bind(on_press=self.login)
        self.register_button.bind(on_press=self.goto_register)

        self.add_widget(self.layout)

    def login(self, instance):
        username = self.spinner.text
        if self.user_repo.user_exists(username):
            self.manager.current_user = username
            self.manager.current = 'main_menu'

    def goto_register(self, instance):
        self.manager.current = 'register'

# Экран регистрации
class RegisterScreen(Screen):
    def __init__(self, user_repo, **kwargs):
        super().__init__(**kwargs)
        self.user_repo = user_repo
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.input = TextInput(hint_text=config.REGISTER_SCREEN_USER_NAME_INPUT_HINT_TEXT, multiline=False)
        self.submit_button = Button(text=config.LOGIN_SCREEN_LOGIN_BUTTON_TEXT)

        self.layout.add_widget(self.input)
        self.layout.add_widget(self.submit_button)

        self.submit_button.bind(on_press=self.register)

        self.add_widget(self.layout)

    def register(self, instance):
        username = self.input.text.strip()
        if username and not self.user_repo.user_exists(username):
            self.user_repo.add_user(username)
            self.manager.current_user = username
            self.manager.get_screen('login').spinner.values = self.user_repo.get_usernames()
            self.manager.current = 'main_menu'

# Главное меню
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_title = StringProperty(config.MAIN_MENU_SCREEN_MAIN_MENU_LABEL_TEXT)
        self.show_dictionary_text = StringProperty(config.MAIN_MENU_SCREEN_SHOW_DICTIONARY_BUTTON_TEXT)
        self.show_training_text = StringProperty(config.MAIN_MENU_SCREEN_SHOW_TRAINING_BUTTON_TEXT)
        # layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        # layout.add_widget(Label(text=config.MAIN_MENU_SCREEN_MAIN_MENU_LABEL_TEXT))
        # layout.add_widget(Button(text=config.MAIN_MENU_SCREEN_SHOW_DICTIONARY_BUTTON_TEXT))
        # layout.add_widget(Button(text=config.MAIN_MENU_SCREEN_SHOW_TRAINING_BUTTON_TEXT))
        # self.add_widget(layout)

# Менеджер экранов
class LangPulseApp(App):
    def build(self):
        self.user_repo = UserRepository()
        self.sm = ScreenManager()
        self.sm.current_user = None
        Builder.load_file("styles/main_menu.kv")

        self.sm.add_widget(LoginScreen(name='login', user_repo=self.user_repo))
        self.sm.add_widget(RegisterScreen(name='register', user_repo=self.user_repo))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))

        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm
