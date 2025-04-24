from typing import Protocol
from kivy.uix.widget import Widget

class SupportsAddWidget(Protocol):
    def add_widget(self, widget: Widget) -> None: ...
