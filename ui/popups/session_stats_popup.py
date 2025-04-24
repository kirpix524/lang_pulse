from kivy.uix.label import Label
from kivy.uix.popup import Popup

from app.config import TrainingDirection
from models.stats import StatsRow


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
