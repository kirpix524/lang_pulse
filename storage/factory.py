import app.config as config
from storage.file.dictionary_file_storage import DictionaryFileStorage
from storage.file.language_file_storage import LanguageFileStorage
from storage.file.session_file_storage import SessionFileStorage
from storage.file.stats_file_storage import StatsFileStorage
from storage.file.user_file_storage import UserFileStorage
from storage.file.word_file_storage import WordFileStorage


def create_file_storage():
    return {
        "users": UserFileStorage(config.FILE_NAMES),
        "languages": LanguageFileStorage(config.FILE_NAMES),
        "words": WordFileStorage(config.WORD_REPO_DATA),
        "dictionaries": DictionaryFileStorage(config.DICTIONARY_DATA),
        "sessions": SessionFileStorage(config.SESSIONS_DATA),
        "stats": StatsFileStorage(config.STATS_DATA)
    }

def create_storage():
    return create_file_storage()