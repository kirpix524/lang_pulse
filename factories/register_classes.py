from factories.word_factory import WordFactory
from models.word import EnglishWord

def register_classes():
    WordFactory.register("en", EnglishWord)