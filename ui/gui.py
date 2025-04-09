from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from storage.db import DBFile
from storage.user_repo import UserRepository

# Экран выбора пользователя
class LoginScreen(Screen):
    def __init__(self, user_repo, **kwargs):
        super().__init__(**kwargs)
        self.user_repo = user_repo
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.spinner = Spinner(text='Выберите пользователя', values=self.user_repo.get_usernames())
        self.login_button = Button(text='Войти')
        self.register_button = Button(text='Зарегистрироваться')

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

        self.input = TextInput(hint_text='Введите имя пользователя', multiline=False)
        self.submit_button = Button(text='Создать и войти')

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
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Главное меню'))
        layout.add_widget(Button(text='Показать словарь'))
        layout.add_widget(Button(text='Показать тренировки'))
        self.add_widget(layout)

# Менеджер экранов
class LangPulseApp(App):
    def build(self):
        self.user_repo = UserRepository()
        self.sm = ScreenManager()
        self.sm.current_user = None

        self.sm.add_widget(LoginScreen(name='login', user_repo=self.user_repo))
        self.sm.add_widget(RegisterScreen(name='register', user_repo=self.user_repo))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))

        return self.sm
