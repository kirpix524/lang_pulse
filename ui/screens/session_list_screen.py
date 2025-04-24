from kivy.uix.button import Button

from models.session import Session
from ui.gui import add_col_label
from ui.screens.base_screen import BaseScreen


class SessionListScreen(BaseScreen):
    """Экран списка тренировок"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.show_sessions()

    def new_session(self):
        """Обработка нажатия кнопки "Новая тренировка" """
        self.ctx.get_session_repo().new_session()
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

        sessions = self.ctx.get_session_repo().get_sessions()
        for session in sessions:
            self.add_session_row(container, session)
