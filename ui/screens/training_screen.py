import time

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty

from app.config import TrainingDirection
from ui.popups.session_stats_popup import SessionStatsPopup
from ui.screens.base_screen import BaseScreen


class TrainingScreen(BaseScreen):
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
        self.ctx.stats_storage.save_training_stats(self.state.get_session(), training)
        self.ctx.session_storage.save_all_sessions(self.state.get_user(), self.state.get_language(), self.ctx.get_session_repo().get_sessions())
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

        if training.direction == TrainingDirection.TO_RU or training.direction == TrainingDirection.RAPID:
            self.training_text = word.word.term
        else:
            self.training_text = word.word.translation

        if training.direction == TrainingDirection.RAPID:
            self._tick = Clock.schedule_once(self.next_word, training.interval)
            self.start_pb_timer(training.interval)
        else:
            self._tick = Clock.schedule_once(self.show_translation, training.interval)
            self.start_pb_timer(training.interval)

    def show_translation(self, *_):
        training = self.state.get_session().get_current_training()
        current_word = training.get_current_word()

        if not current_word or self.translation_visible:
            return

        if training.direction == TrainingDirection.TO_RU:
            self.training_text += f"\n[перевод: {current_word.word.translation}]"
        else:
            self.training_text += f"\n[перевод: {current_word.word.term}]"

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
            if training.direction == TrainingDirection.RAPID:
                training.pop_word()
                self.next_step()
                return
            training.mark_remembered()
            self.next_step()
        elif key == 32:  # Space
            Clock.unschedule(self._tick)
            self.stop_pb_timer()
            if training.direction == TrainingDirection.RAPID:
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
