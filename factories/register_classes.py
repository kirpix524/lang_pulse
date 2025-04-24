from factories.dictionary_screen_renderer_factory import DictionaryWordRowRendererFactory
from factories.user_word_factory import UserWordFactory
from factories.word_factory import WordFactory
from models.user_word import EnglishUserWord
from models.word import EnglishWord
from ui.renderers.user_dictionary_renderers import EnglishDictionaryWordRowRenderer


def register_classes():
    WordFactory.register("en", EnglishWord)
    UserWordFactory.register("en", EnglishUserWord)
    DictionaryWordRowRendererFactory.register("en", EnglishDictionaryWordRowRenderer)