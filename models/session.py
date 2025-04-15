from models.dictionary import Dictionary, Word


class Session:
    def __init__(self, dictionary: Dictionary, session_id: int, words: list[Word]):
        self.__dictionary = dictionary
        self.__session_id = session_id
        self.__words = words

    def add_word(self, word: Word):
        self.__words.append(word)

    def get_words(self):
        return self.__words

    def get_id(self):
        return self.__session_id