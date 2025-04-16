import random
from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import storage.config as config
from models.dictionary import Dictionary, Word
from storage.db import db
from storage.session_repo import SessionRepository
from models.app import AppState
from datetime import datetime

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



class MessagePopup(Popup):
    def set_message(self, message):
        # Устанавливаем текст сообщения
        self.ids.message_label.text = message

    def set_title(self, title):
        # Устанавливаем заголовок сообщения
        self.title = title

class AddNewWordPopup(Popup):
    def __init__(self, dictionary, on_success=None, **kwargs):
        super().__init__(**kwargs)
        self.dictionary = dictionary
        self.on_success = on_success

    def add_new_word(self):
        term = self.ids.word_input.text.strip()
        transcription = self.ids.transcription_input.text.strip()
        translation = self.ids.translation_input.text.strip()

        if term and translation:
            self.dictionary.add_word(Word(term, translation, transcription, datetime.now()))
            db.save_dictionary(self.dictionary)
            self.dismiss()
            if self.on_success:
                self.on_success()

class ChooseWordsPopup(Popup):
    def __init__(self, words, on_words_selected, **kwargs):
        super().__init__(**kwargs)
        self.words = words
        self.on_words_selected = on_words_selected
        self.checkboxes = {}
        self.populate_word_list()

    def populate_word_list(self):
        grid = self.ids.words_grid
        grid.clear_widgets()

        # Заголовки
        grid.add_widget(Label(text='', bold=True))
        for header in ["Слово", "Транскрипция", "Перевод", "Добавлено", "Последнее повторение"]:
            grid.add_widget(Label(text=header, bold=True, color=(0, 0, 0, 1)))

        for word in self.words:
            cb = CheckBox(size_hint=(None, None), size=(30, 30))
            self.checkboxes[word] = cb
            grid.add_widget(cb)

            grid.add_widget(Label(text=word.word))
            grid.add_widget(Label(text=word.transcription or ''))
            grid.add_widget(Label(text=word.translation))
            grid.add_widget(Label(text=word.added_at.strftime('%Y-%m-%d %H:%M') if word.added_at else ''))
            grid.add_widget(Label(text=word.last_repeated_at.strftime('%Y-%m-%d %H:%M') if word.last_repeated_at else ''))

    def select_words(self):
        selected = [word for word, cb in self.checkboxes.items() if cb.active]
        self.on_words_selected(selected)
        self.dismiss()

class DirectionSelectPopup(Popup):
    def __init__(self, on_selected, **kwargs):
        super().__init__(**kwargs)
        self.on_selected = on_selected

    def choose(self, direction):
        self.dismiss()
        if self.on_selected:
            self.on_selected(direction)


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
                self.state.set_dictionary(db.load_dictionary(self.state.get_user(), self.state.get_language()))
                self.state.set_session_repo(SessionRepository(self.state.get_dictionary()))
                self.manager.current = 'main_menu'
            else:
                show_message("Ошибка",'Нужно выбрать язык')
        else:
            show_message("Ошибка",'Пользователь не выбран')

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
                self.goto_screen('login')
            else:
                show_message("Ошибка","Такое имя пользователя уже есть")
        else:
            show_message("Ошибка","Введите имя пользователя")


# Главное меню
class MainMenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DictionaryScreen(BaseScreen):
    """Экран словаря"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_word(self):
        """Обрабатывает нажатие кнопки "Добавить слово" """
        popup = AddNewWordPopup(self.state.get_dictionary(), on_success=self.show_words)
        popup.open()

    def on_pre_enter(self):
        super().on_pre_enter()
        self.show_words()

    def show_words(self):
        """Показывает слова в таблице"""
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
            add_col_label(container, word.added_at.strftime('%d.%m.%Y %H:%M') if word.added_at else '')
            add_col_label(container, word.last_repeated_at.strftime('%d.%m.%Y %H:%M') if word.last_repeated_at else '')

class SessionListScreen(BaseScreen):
    """Экран списка тренировок"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.show_sessions()

    def new_session(self):
        """Обработка нажатия кнопки "Новая тренировка" """
        self.state.get_session_repo().new_session()
        self.show_sessions()
        self.goto_screen('session_list')

    def add_session_row(self, container, session):
        def on_click(instance):
            self.state.set_session(session)
            self.goto_screen('session')

        btn = Button(
            text=session.get_session_name() or "Без имени",
            size_hint_y=None,
            height=30,
            size_hint_x=None,
            width=150,
            on_press=on_click,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0, 0, 0, 1)
        )
        container.add_widget(btn)
        add_col_label(container, session.get_created_at().strftime('%d.%m.%Y %H:%M'))
        add_col_label(container, session.get_last_repeated_at().strftime(
            '%d.%m.%Y %H:%M') if session.get_last_repeated_at() else '')

    def show_sessions(self):
        """Вывод на экран списка тренировок"""
        container = self.ids.sessions_container
        container.clear_widgets()
        headers = ["Тренировка", "Добавлено", "Последнее повторение"]
        for title in headers:
            add_col_label(container, title)

        sessions = self.state.get_session_repo().get_sessions()
        for session in sessions:
            self.add_session_row(container, session)

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
            add_col_label(self.ids.words_container, word.word)

    def start_session(self):
        interval_text = self.ids.interval_input.text.strip()

        if not interval_text or not interval_text.isdigit():
            show_message("Ошибка", "Введите корректный интервал в секундах")
            return

        interval = float(interval_text)
        session = self.state.get_session()

        if not session or len(session.get_words())<5:
            show_message("Ошибка", "Добавьте не менее 5 слов в тренировку")
            return

        def on_direction_chosen(direction):
            session.set_interval(interval)
            session.set_direction(direction)
            self.goto_screen('session_training')

        popup = DirectionSelectPopup(on_selected=on_direction_chosen)
        popup.open()

    def add_words_to_session(self):
        # Реализация добавления слова в тренировку
        dictionary = self.state.get_dictionary()
        session = self.state.get_session()

        if not dictionary or not session:
            show_message("Ошибка", "Словарь или тренировка не найдены")

        available_words = session.get_words_not_in_session()

        def on_added(words):
            session.add_words(words)
            db.save_all_sessions(self.state.get_dictionary(), self.state.get_session_repo().get_sessions())
            self.show_words()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_added)
        popup.open()

    def remove_words_from_session(self):
        # Реализация удаления слова из тренировки
        session = self.state.get_session()

        if not session:
            show_message("Ошибка", "Словарь или тренировка не найдены")

        available_words = session.get_words()

        def on_deleted(words):
            session.del_words(words)
            db.save_all_sessions()
            self.show_words()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_deleted)
        popup.open()

class SessionTrainingScreen(BaseScreen):
    training_text = StringProperty("")
    translation_visible = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tick = None

    def on_pre_enter(self):
        super().on_pre_enter()
        Window.bind(on_key_down=self._on_key_down)
        self.start_training()

    def on_leave(self):
        Window.unbind(on_key_down=self._on_key_down)
        self.training_text = ""
        self.translation_visible = False
        if self._tick:
            Clock.unschedule(self._tick)

    def start_training(self):
        session = self.state.get_session()
        interval = session.get_interval() or 3
        direction = session.get_direction() or "to_ru"

        session.start_training(direction, interval)
        self.next_step()

    def next_step(self, *_):
        session = self.state.get_session()

        if session.is_complete():
            self.training_text = "🎉 Тренировка завершена"
            return

        word = session.get_next_word()
        if not word:
            self.training_text = "⚠ Нет слов"
            return

        self.translation_visible = False

        if session.get_direction() == "to_ru":
            self.training_text = word.word
        else:
            self.training_text = word.translation

        self._tick = Clock.schedule_once(self.show_translation, session.get_interval())

    def show_translation(self, *_):
        session = self.state.get_session()
        word = session.get_current_word()

        if not word or self.translation_visible:
            return

        if session.get_direction() == "to_ru":
            self.training_text += f"\n[перевод: {word.translation}]"
        else:
            self.training_text += f"\n[перевод: {word.word}]"

        self.translation_visible = True

        # Переместить слово назад в списке
        session.mark_forgotten()
        Clock.schedule_once(self.next_step, 2)

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if self.state.get_session().is_complete():
            return

        if key == 13:  # Enter
            Clock.unschedule(self._tick)
            self.state.get_session().mark_remembered()
            self.next_step()
        elif key == 32:  # Space
            Clock.unschedule(self._tick)
            self.show_translation()


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
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}session_list.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}shared_widgets.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}message_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}add_new_word_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}choose_words_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}direction_select_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}session.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}session_training.kv")
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(DictionaryScreen(name='dictionary'))
        self.sm.add_widget(SessionListScreen(name='session_list'))
        self.sm.add_widget(SessionScreen(name='session'))
        self.sm.add_widget(SessionTrainingScreen(name='session_training'))

        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm
