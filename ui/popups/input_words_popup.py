from kivy.uix.popup import Popup


class InputWordPopup(Popup):
    def __init__(self, on_input_finished=None, **kwargs):
        super().__init__(**kwargs)
        self.on_input_finished = on_input_finished

    def finish_input(self):
        term = self.ids.word_input.text.strip()
        translation = self.ids.translation_input.text.strip()

        if term and translation:
            if self.on_input_finished:
                self.on_input_finished(term, translation)
        self.dismiss()

class InputEnglishWordPopup(InputWordPopup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def finish_input(self):
        term = self.ids.word_input.text.strip()
        transcription = self.ids.transcription_input.text.strip()
        translation = self.ids.translation_input.text.strip()

        if term and translation:
            if self.on_input_finished:
                self.on_input_finished(term, translation, transcription)
        self.dismiss()