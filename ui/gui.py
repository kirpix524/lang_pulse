import os

from screeninfo import get_monitors
from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label

import app.config as config
from app.state import AppState
from app.context import AppContext
from ui.popups.message_popup import MessagePopup
from ui.screens.login_screen import LoginScreen
from ui.screens.main_menu_screen import MainMenuScreen
from ui.screens.register_screen import RegisterScreen
from ui.screens.session_list_screen import SessionListScreen
from ui.screens.session_screen import SessionScreen
from ui.screens.training_screen import TrainingScreen
from ui.screens.user_dictionary_screen import UserDictionaryScreen
from ui.screens.word_stats_screen import WordStatsScreen


def show_message(title: str, message: str):
    popup = MessagePopup()
    popup.set_message(message)
    popup.set_title(title)
    popup.open()

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

def load_all_kv_files(directory: str):
    for filename in os.listdir(directory):
        if filename.endswith(".kv"):
            path = os.path.join(directory, filename)
            Builder.load_file(path)

# Менеджер экранов
class LangPulseApp(App):
    def register_screens(self):
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(UserDictionaryScreen(name='dictionary'))
        self.sm.add_widget(SessionListScreen(name='session_list'))
        self.sm.add_widget(SessionScreen(name='session'))
        self.sm.add_widget(TrainingScreen(name='session_training'))
        self.sm.add_widget(WordStatsScreen(name='word_stats'))

    def build(self):
        self.state = AppState()
        self.ctx = AppContext()
        self.sm = ScreenManager()
        self.sm.state = self.state
        self.sm.ctx = self.ctx

        load_all_kv_files(config.LAYOUTS_DIRECTORY)
        self.register_screens()

        monitors = get_monitors()
        if len(monitors) >= 2:
            second = monitors[1]
            Window.left = second.x - 2100
            Window.top = second.y
        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm


