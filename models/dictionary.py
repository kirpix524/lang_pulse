from models.language import Language
from models.user import User
from storage.db import db


class Word:
    def __init__(self, word, translation, transcription):
        self.word = word
        self.translation = translation
        self.transcription = transcription


class Dictionary:
    def __init__(self, user: User, language: Language):
        self.__user = user
        self.__language = language
        self.__words = db.load_dictionary(self)

    def set_user(self, user: User):
        self.__user = user

    def set_language(self, language: Language):
        self.__language = language

    def get_user(self):
        return self.__user

    def get_language(self):
        return self.__language

    def get_words(self):
        return self.__words

    def add_word(self, word: Word):
        self.__words.append(word)
        db.save_dictionary(self)