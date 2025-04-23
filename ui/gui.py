from screeninfo import get_monitors
import time
from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

import app.config as config
from models.user_word import IBasicUserWord
from models.session import Session
from repositories.session_repo import SessionRepository
from app.state import AppState
from app.config import TrainingDirection
from models.stats import StatsRow


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


class TimerBar(Widget):
    progress = NumericProperty(1.0)  # от 1.0 до 0.0

    __events__ = ("on_complete",)  # 👈 регистрация пользовательского события

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event = None
        self._remaining = None
        self._interval = None
        with self.canvas.before:
            self.color = Color(0, 1, 0, 1)  # зелёный
            self.rect = RoundedRectangle (pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect, progress=self._update_rect)

    def _update_rect(self, *args):
        full_width = self.width
        self.rect.pos = self.pos
        self.rect.size = (full_width * self.progress, self.height)
        # Обновим цвет: от зелёного к жёлтому, затем к красному
        if self.progress > 0.5:
            # от зелёного (0,1,0) к жёлтому (1,1,0)
            r = 2 * (1 - self.progress)
            self.color.rgba = (r, 1, 0, 1)
        else:
            # от жёлтого (1,1,0) к красному (1,0,0)
            g = 2 * self.progress
            self.color.rgba = (1, g, 0, 1)

    def start(self, interval: float):
        self.progress = 1.0
        self._interval = interval
        self._remaining = interval
        self._event = Clock.schedule_interval(self._tick, 0.05)

    def stop(self):
        if hasattr(self, '_event') and self._event:
            self._event.cancel()

    def _tick(self, dt):
        self._remaining -= dt
        self.progress = max(0, self._remaining / self._interval)
        if self._remaining <= 0:
            self._event.cancel()
            self.dispatch("on_complete")

    def on_complete(self):
        pass  # перехватывается в родителе, если нужно

    def cancel(self):
        if hasattr(self, '_event') and self._event:
            self._event.cancel()

class MessagePopup(Popup):
    def set_message(self, message):
        # Устанавливаем текст сообщения
        self.ids.message_label.text = message

    def set_title(self, title):
        # Устанавливаем заголовок сообщения
        self.title = title

class InputWordPopup(Popup):
    def __init__(self, on_input_finished=None, **kwargs):
        super().__init__(**kwargs)
        self.on_input_finished = on_input_finished

    def finish_input(self):
        term = self.ids.word_input.text.strip()
        transcription = self.ids.transcription_input.text.strip()
        translation = self.ids.translation_input.text.strip()

        if term and translation:
            if self.on_input_finished:
                self.on_input_finished(term, translation, transcription)
        self.dismiss()

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
            grid.add_widget(Label(text=header, bold=True))

        for word in self.words:
            cb = CheckBox(size_hint=(None, None), size=(30, 30))
            self.checkboxes[word] = cb
            grid.add_widget(cb)

            grid.add_widget(Label(text=word.word, size_hint_x=None, width=150))
            grid.add_widget(Label(text=word.get_transcription(), size_hint_x=None, width=150))
            grid.add_widget(Label(text=word.translation, size_hint_x=None, width=150))
            grid.add_widget(Label(text=word.get_added_at_str(), size_hint_x=None, width=100))
            grid.add_widget(Label(text=word.get_last_repeated_at_str(), size_hint_x=None, width=100))

    def select_words(self):
        selected = [word for word, cb in self.checkboxes.items() if cb.active]
        self.on_words_selected(selected)
        self.dismiss()

class DirectionSelectPopup(Popup):
    to_ru = TrainingDirection.TO_RU
    to_foreign = TrainingDirection.TO_FOREIGN
    rapid = TrainingDirection.RAPID
    def __init__(self, on_selected, **kwargs):
        super().__init__(**kwargs)
        self.on_selected = on_selected

    def choose(self, direction):
        self.dismiss()
        if self.on_selected:
            self.on_selected(direction)

class SessionStatsPopup(Popup):
    def __init__(self, stats: list[StatsRow], on_dismiss=None, **kwargs):
        super().__init__(**kwargs)
        self.stats = stats
        self.populate_table()

    def populate_table(self):
        grid = self.ids.stats_grid
        grid.clear_widgets()

        # Заголовки
        headers = ["Слово", "Перевод", "Результат", "Время"]
        for header in headers:
            grid.add_widget(Label(
                text=header,
                bold=True,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=30
            ))

        for row in self.stats:
            if row.direction==TrainingDirection.RAPID:
                text_result = ""
            else:
                text_result = "Правильно" if row.success else "Неправильно"

            grid.add_widget(Label(text=row.word, size_hint_x=None, size_hint_y=None, width=150, height=30))
            grid.add_widget(Label(text=row.translation, size_hint_x=None, size_hint_y=None, width=150, height=30))
            grid.add_widget(Label(text=text_result, size_hint_x=None, size_hint_y=None, width=150, height=30))
            grid.add_widget(Label(text=f"{row.recall_time} сек" if row.recall_time else "-", size_hint_x=None, size_hint_y=None, width=100, height=30))

    def on_leave(self):
        if self.on_dismiss:
            self.on_dismiss()

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

                self.state.set_dictionary(self.state.dictionary_storage.load_dictionary(self.state.get_user(), self.state.get_language()))
                self.state.stats_storage.load_training_stats_words(self.state.get_user(), self.state.get_language(), self.state.get_dictionary())
                self.state.get_session_repo().set_session_scope(self.state.get_user(), self.state.get_language(), self.state.get_dictionary())
                self.goto_screen('main_menu')
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
        def save_word(term, translation, transcription):
            self.state.get_dictionary().add_word(term, translation, transcription=transcription)
            self.state.dictionary_storage.save_dictionary(self.state.get_dictionary())
            self.show_words()
        popup = InputWordPopup(on_input_finished=save_word)
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
            add_col_label(container, f"[{word.get_transcription()}]")
            add_col_label(container, word.translation)
            add_col_label(container, word.get_added_at_str())
            add_col_label(container, word.get_last_repeated_at_str())

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

    def add_session_row(self, container, session: Session):
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
        add_col_label(container, session.get_created_at_str())
        add_col_label(container, session.get_last_repeated_at_str())
        add_col_label(container, str(session.get_total_trainings()) )

    def show_sessions(self):
        """Вывод на экран списка тренировок"""
        container = self.ids.sessions_container
        container.clear_widgets()
        headers = ["Сессия", "Добавлено", "Последнее повторение", "Всего тренировок"]
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

    def start_training(self):
        interval_text = self.ids.interval_input.text.strip()

        if not interval_text:
            show_message("Ошибка", "Введите интервал в секундах")
            return

        interval = float(interval_text)
        session = self.state.get_session()

        if not session or len(session.get_words())<5:
            show_message("Ошибка", "Добавьте не менее 5 слов в тренировку")
            return



        def on_direction_chosen(direction):
            session.add_new_training(direction, interval)
            self.goto_screen('session_training')

        popup = DirectionSelectPopup(on_selected=on_direction_chosen)
        popup.open()

    def add_words_to_session(self):
        # Реализация добавления слова в тренировку
        session = self.state.get_session()
        if not session.can_be_changed():
            show_message("Ошибка", "Эта тренировка уже запускалась и ее нельзя изменять")
            return
        dictionary = self.state.get_dictionary()

        if not dictionary or not session:
            show_message("Ошибка", "Словарь или тренировка не найдены")

        available_words = dictionary.get_words_not_in_list(session.get_words())

        def on_added(words):
            session.add_words(words)
            self.state.session_storage.save_all_sessions(self.state.get_user(), self.state.get_language(), self.state.get_session_repo().get_sessions())
            self.show_words()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_added)
        popup.open()

    def remove_words_from_session(self):
        # Реализация удаления слова из тренировки
        session = self.state.get_session()
        if not session.can_be_changed():
            show_message("Ошибка", "Эта тренировка уже запускалась и ее нельзя изменять")
            return

        if not session:
            show_message("Ошибка", "Словарь или тренировка не найдены")

        available_words = session.get_words()

        def on_deleted(words):
            session.del_words(words)
            self.state.session_storage.save_all_sessions(self.state.get_user(), self.state.get_language(), self.state.get_session_repo().get_sessions())
            self.show_words()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_deleted)
        popup.open()

class SessionTrainingScreen(BaseScreen):
    training_text = StringProperty("")
    translation_visible = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remaining_time = None
        self._progress_event = None
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
        self.stop_pb_timer()

    def start_training(self):
        self.next_step()

    def finish_training(self):
        Window.unbind(on_key_down=self._on_key_down)
        self.training_text = "🎉 Тренировка завершена"
        training = self.state.get_session().get_current_training()
        # Сохранить статистику
        self.state.stats_storage.save_training_stats(self.state.get_session(), training)
        self.state.session_storage.save_all_sessions(self.state.get_user(), self.state.get_language(), self.state.get_session_repo().get_sessions())
        self.state.get_dictionary().update_training_stats(training.get_stats())
        # Показать статистику
        popup = SessionStatsPopup(stats=training.get_stats(), on_dismiss=self.goto_screen('session'))
        popup.open()

    def next_step(self, *_):
        training = self.state.get_session().get_current_training()

        if training.is_complete():
            self.finish_training()
            return

        word = training.get_next_word()
        if not word:
            self.training_text = "⚠ Нет слов"
            return
        else:
            word.set_start_time(time.time())

        self.translation_visible = False

        if training.get_direction() == TrainingDirection.TO_RU or training.get_direction() == TrainingDirection.RAPID:
            self.training_text = word.word
        else:
            self.training_text = word.translation

        if training.get_direction() == TrainingDirection.RAPID:
            self._tick = Clock.schedule_once(self.next_word, training.get_interval())
            self.start_pb_timer(training.get_interval())
        else:
            self._tick = Clock.schedule_once(self.show_translation, training.get_interval())
            self.start_pb_timer(training.get_interval())

    def show_translation(self, *_):
        training = self.state.get_session().get_current_training()
        word = training.get_current_word()

        if not word or self.translation_visible:
            return

        if training.get_direction() == TrainingDirection.TO_RU:
            self.training_text += f"\n[перевод: {word.translation}]"
        else:
            self.training_text += f"\n[перевод: {word.word}]"

        self.translation_visible = True

        # Переместить слово назад в списке
        training.mark_forgotten()
        self._tick = Clock.schedule_once(self.next_step, 2)

    def next_word(self, *_):
        self.state.get_session().get_current_training().pop_word()
        self.next_step()

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        training = self.state.get_session().get_current_training()
        if training.is_complete():
            return

        if key == 13:  # Enter
            Clock.unschedule(self._tick)
            self.stop_pb_timer()
            if self.translation_visible:  #Если показан перевод, значит ранее пользователь нажал пробел, при следующем нажатии идем к следующему слову
                self.next_step()
                return
            if training.get_direction() == TrainingDirection.RAPID:
                training.pop_word()
                self.next_step()
                return
            training.mark_remembered()
            self.next_step()
        elif key == 32:  # Space
            Clock.unschedule(self._tick)
            self.stop_pb_timer()
            if training.get_direction() == TrainingDirection.RAPID:
                training.pop_word()
                self.next_step()
                return
            if self.translation_visible:  #Если показан перевод, значит ранее пользователь нажал пробел, при следующем нажатии идем к следующему слову
                self.next_step()
                return
            self.show_translation()

    def start_pb_timer(self, interval):
        self.ids.timer_bar.start(interval)

    def stop_pb_timer(self):
        self.ids.timer_bar.stop()

class WordStatsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__words_for_stats: list[IBasicUserWord] = []
        self.__stats_user = None
        self.__stats_language = None


    def on_pre_enter(self):
        super().on_pre_enter()
        if self.__stats_user != self.state.get_user() or self.__stats_language != self.state.get_language():
            self.__words_for_stats.clear()
            self.__stats_user = self.state.get_user()
            self.__stats_language = self.state.get_language()
        self.show_stats()

    def add_words_for_stats(self):
        dictionary = self.state.get_dictionary()
        if not dictionary:
            return

        available_words = [w for w in dictionary.get_words() if w not in self.__words_for_stats]

        def on_added(words):
            self.__words_for_stats.extend(words)
            self.show_stats()

        popup = ChooseWordsPopup(words=available_words, on_words_selected=on_added)
        popup.open()

    def remove_words_for_stats(self):
        if not self.__words_for_stats:
            return

        def on_removed(words):
            for w in words:
                if w in self.__words_for_stats:
                    self.__words_for_stats.remove(w)
            self.show_stats()

        popup = ChooseWordsPopup(words=self.__words_for_stats, on_words_selected=on_removed)
        popup.open()

    def show_stats(self):
        container = self.ids.stats_container
        container.clear_widgets()

        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=5)
        header.add_widget(Label(text="Результат", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100))
        header.add_widget(Label(text="Время", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100))
        header.add_widget(Label(text="Дата", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=140))
        header.add_widget(Label(text="Направление", font_size='22sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=80))
        container.add_widget(header)

        for word in self.__words_for_stats:
            stats = word.get_stats()
            container.add_widget(self.create_word_row(word))
            if not stats:
                continue

            for stat in stats:
                container.add_widget(self.create_stat_row(stat))

    def create_word_row(self, word: IBasicUserWord):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=5)

        row.add_widget(Label(text=word.word, font_size='18sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text=word.translation, font_size='18sp', bold=True, color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text='', size_hint_x=None, width=140, size_hint_y=None, height=30))
        row.add_widget(Label(text='', size_hint_x=None, width=80, size_hint_y=None, height=30))
        return row

    def create_stat_row(self, stat: StatsRow):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=5)

        row.add_widget(Label(text="Правильно" if stat.success else "Неправильно", color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text=f"{stat.recall_time}s" if stat.recall_time else "-", color=(0, 0, 0, 1), size_hint_x=None, width=100, size_hint_y=None, height=30))
        row.add_widget(Label(text=stat.get_timestamp_str(), color=(0, 0, 0, 1), size_hint_x=None, width=140, size_hint_y=None, height=30))
        row.add_widget(Label(text=stat.get_direction_name(), color=(0, 0, 0, 1), size_hint_x=None, width=80))

        return row

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
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}input_word_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}choose_words_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}direction_select_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}session_stats_popup.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}session.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}session_training.kv")
        Builder.load_file(f"{config.LAYOUTS_DIRECTORY}word_stats.kv")
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(DictionaryScreen(name='dictionary'))
        self.sm.add_widget(SessionListScreen(name='session_list'))
        self.sm.add_widget(SessionScreen(name='session'))
        self.sm.add_widget(SessionTrainingScreen(name='session_training'))
        self.sm.add_widget(WordStatsScreen(name='word_stats'))

        monitors = get_monitors()
        if len(monitors) >= 2:
            second = monitors[1]
            Window.left = second.x - 2100
            Window.top = second.y
        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        return self.sm
