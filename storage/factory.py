import app.config as config
from storage.file.dictionary_file_storage import UserDictionaryFileStorage
from storage.file.language_file_storage import LanguageFileStorage
from storage.file.session_file_storage import SessionFileStorage
from storage.file.stats_file_storage import StatsFileStorage
from storage.file.user_file_storage import UserFileStorage
from storage.file.word_file_storage import WordFileStorage
from storage.sqlite.dictionary_sqlite_storage import UserDictionarySQLiteStorage
from storage.sqlite.language_sqlite_storage import LanguageSqliteStorage
from storage.sqlite.session_sqlite_storage import SessionSQLiteStorage
from storage.sqlite.stats_sqlite_storage import StatsSQLiteStorage
from storage.sqlite.user_sqlite_storage import UserSQLiteStorage
from storage.sqlite.word_sqlite_storage import WordSQLiteStorage


def create_file_storage():
    return {
        "users": UserFileStorage(config.FILE_NAMES),
        "languages": LanguageFileStorage(config.FILE_NAMES),
        "words": WordFileStorage(config.WORD_REPO_DATA),
        "user_dictionaries": UserDictionaryFileStorage(config.DICTIONARY_DATA),
        "sessions": SessionFileStorage(config.SESSIONS_DATA),
        "stats": StatsFileStorage(config.STATS_DATA)
    }

def create_sqlite_storage():
    return {
        "users": UserSQLiteStorage(config.SQL_DATA),
        "languages": LanguageSqliteStorage(config.SQL_DATA),
        "words": WordSQLiteStorage(config.SQL_DATA),
        "user_dictionaries": UserDictionarySQLiteStorage(config.SQL_DATA),
        "sessions": SessionSQLiteStorage(config.SQL_DATA),
        "stats": StatsSQLiteStorage(config.SQL_DATA)
    }

def create_storage():
    #return create_file_storage()
    return create_sqlite_storage()