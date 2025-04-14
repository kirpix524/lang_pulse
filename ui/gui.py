from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
import storage.config as config
from models.dictionary import Dictionary, Word
from storage.db import db
from storage.user_repo import UserRepository
from models.user import User
from models.app import AppState


def show_error(message: str):
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button

    layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    layout.add_widget(Label(text=message))

    close_button = Button(text='Закрыть', size_hint=(1, 0.3))
    layout.add_widget(close_button)

    popup = Popup(title='Ошибка',
                  content=layout,
                  size_hint=(None, None),
                  size=(300, 200),
                  auto_dismiss=False)
    close_button.bind(on_press=popup.dismiss)
    popup.open()

def open_add_word_popup(dictionary:Dictionary, on_success=None):
    from kivy.uix.popup import Popup
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    word_input = TextInput(hint_text="Слово", multiline=False)
    transcription_input = TextInput(hint_text="Транскрипция", multiline=False)
    translation_input = TextInput(hint_text="Перевод", multiline=False)

    def on_add(instance):
        term = word_input.text.strip()
        transcription = transcription_input.text.strip()
        translation = translation_input.text.strip()

        if term and translation:
            dictionary.add_word(Word(term, translation, transcription))
            db.save_dictionary(dictionary)
            popup.dismiss()
            if on_success:
                on_success()  # <<< вызываем колбэк

    add_button = Button(text="Добавить", size_hint_y=None, height=40)
    add_button.bind(on_press=on_add)

    layout.add_widget(Label(text="Добавление слова", size_hint_y=None, height=30))
    layout.add_widget(word_input)
    layout.add_widget(transcription_input)
    layout.add_widget(translation_input)
    layout.add_widget(add_button)

    popup = Popup(
        title="Новое слово",
        content=layout,
        size_hint=(None, None),
        size=(400, 400),
        auto_dismiss=True
    )
    popup.open()


class BaseScreen(Screen):
    current_user_name = StringProperty('')
    current_language_name = StringProperty('')
    def on_pre_enter(self):
        if self.state.get_user():
            self.current_user_name = self.state.get_user().username or ''
        if self.state.get_language():
            self.current_language_name = self.state.get_language().lang_name or ''
    def goto_login(self):
        self.manager.current = 'login'

    def goto_main_menu(self):
        self.manager.current = 'main_menu'

    def goto_register(self):
        self.manager.current = 'register'

    def goto_dictionary(self):
        self.manager.current = 'dictionary'

    @property
    def state(self) -> AppState:
        return self.manager.state

# Экран выбора пользователя
class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        """Вызывается при входе на экран"""
        self.ids.username_spinner.values = self.state.get_user_repo().get_usernames()
        self.ids.language_spinner.values = self.state.get_lang_repo().get_language_names()
        if self.state.get_user():
            self.ids.username_spinner.text = str(self.state.get_user().username)
        if self.state.get_language():
            self.ids.language_spinner.text = str(self.state.get_language().lang_name)

    def login(self):
        username = self.ids.username_spinner.text
        lang_name = self.ids.language_spinner.text
        if self.state.get_user_repo().user_exists(username):
            if self.state.get_lang_repo().get_language_by_name(lang_name):
                self.state.set_user(self.state.get_user_repo().get_user_by_name(username))
                self.state.set_language(self.state.get_lang_repo().get_language_by_name(lang_name))
                self.state.set_dictionary(Dictionary(self.state.get_user(), self.state.get_language()))
                db.load_dictionary(self.state.get_dictionary())
                self.manager.current = 'main_menu'
            else:
                show_error('Нужно выбрать язык')
        else:
            show_error('Пользователь не выбран')

# Экран регистрации
class RegisterScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register(self):
        username = self.ids.username_input.text.strip()
        if username:
            if not self.state.get_user_repo().user_exists(username):
                self.state.get_user_repo().add_user(username)
                self.state.set_user(self.state.get_user_repo().get_user_by_name(username))
                self.goto_login()
            else:
                show_error("Такое имя пользователя уже есть")
        else:
            show_error("Введите имя пользователя")


# Главное меню
class MainMenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Экран словаря
def add_col_label(container, title: str):
    container.add_widget(Label(
        text=title,
        bold=True,
        color=(0, 0, 0, 1),
        size_hint_y=None,
        height=30,
        size_hint_x=None,
        width=150
    ))


class DictionaryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_word(self):
        open_add_word_popup(self.state.get_dictionary(), on_success=self.load_words)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.load_words()

    def load_words(self):
        container = self.ids.words_container
        container.clear_widgets()

        if not self.state.get_dictionary():
            return

        words = self.state.get_dictionary().get_words()

        # Заголовки таблицы
        headers = ["Слово", "Транскрипция", "Перевод", "Добавлено", "Последнее повторение"]
        for title in headers:
            add_col_label(container, title)

        for word in words:
            add_col_label(container, word.word)
            add_col_label(container, f"[{word.transcription or ''}]")
            add_col_label(container, word.translation)
            add_col_label(container, word.added_at.strftime('%H:%M %d.%m.%Y') if word.added_at else '')
            add_col_label(container, word.last_repeated_at.strftime('%H:%M %d.%m.%Y') if word.last_repeated_at else '')

# Менеджер экранов
class LangPulseApp(App):
    def build(self):
        self.state = AppState()
        self.sm = ScreenManager()
        self.sm.state = self.state
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}main_menu.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}login.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}register.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}dictionary.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}shared_widgets.kv")
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(DictionaryScreen(name='dictionary'))

        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm
