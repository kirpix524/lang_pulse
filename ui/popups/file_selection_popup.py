from typing import Callable, Optional
from kivy.uix.popup import Popup

class FileSelectionPopup(Popup):
    def __init__(self, on_selection_finished: Optional[Callable[[str], None]] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._on_selection_finished = on_selection_finished

    @property
    def on_selection_finished(self) -> Optional[Callable[[str], None]]:
        return self._on_selection_finished

    def finish_selection(self) -> None:
        selection = self.ids.filechooser.selection
        if selection and self._on_selection_finished:
            self._on_selection_finished(selection[0])
        self.dismiss()
