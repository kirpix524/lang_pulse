from kivy.uix.popup import Popup


class MessagePopup(Popup):
    def set_message(self, message):
        # Устанавливаем текст сообщения
        self.ids.message_label.text = message

    def set_title(self, title):
        # Устанавливаем заголовок сообщения
        self.title = title
