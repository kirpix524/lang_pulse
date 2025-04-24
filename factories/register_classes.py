from factories.dictionary_screen_renderer_factory import DictionaryWordRowRendererFactory
from factories.user_dictionary_screen_renderer_factory import UserDictionaryWordRowRendererFactory
from factories.input_word_popup_factory import InputWordPopupFactory
from factories.user_word_factory import UserWordFactory
from factories.word_factory import WordFactory
from models.user_word import EnglishUserWord
from models.word import EnglishWord
from ui.popups.input_words_popup import InputEnglishWordPopup
from ui.renderers.dictionary_renderers import EnglishDictionaryWordRowRenderer
from ui.renderers.user_dictionary_renderers import EnglishUserDictionaryWordRowRenderer


def register_classes():
    WordFactory.register("en", EnglishWord)
    UserWordFactory.register("en", EnglishUserWord)
    UserDictionaryWordRowRendererFactory.register("en", EnglishUserDictionaryWordRowRenderer)
    InputWordPopupFactory.register("en", InputEnglishWordPopup)
    DictionaryWordRowRendererFactory.register("en", EnglishDictionaryWordRowRenderer)