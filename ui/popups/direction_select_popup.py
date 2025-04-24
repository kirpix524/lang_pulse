from kivy.uix.popup import Popup

from app.config import TrainingDirection


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
