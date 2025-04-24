from repositories.lang_repo import LanguageRepository
from repositories.session_repo import SessionRepository
from repositories.user_repo import UserRepository
from repositories.word_repo import WordRepository
from storage.factory import create_storage
from storage.interfaces import IUserStorage, ILanguageStorage, IUserDictionaryStorage, ISessionStorage, IStatsStorage, \
    IWordStorage


class AppContext:
    user_storage: IUserStorage
    language_storage: ILanguageStorage
    user_dictionary_storage: IUserDictionaryStorage
    session_storage: ISessionStorage
    stats_storage: IStatsStorage
    words_storage: IWordStorage

    def __init__(self):
        storage = create_storage()
        self.user_dictionary_storage = storage["user_dictionaries"]
        self.stats_storage = storage["stats"]
        self.session_storage = storage["sessions"]
        self.user_storage = storage["users"]
        self.language_storage = storage["languages"]
        self.words_storage = storage["words"]
        self.__user_repo = UserRepository(self.user_storage)
        self.__lang_repo = LanguageRepository(self.language_storage)
        self.__word_repo = WordRepository(self.words_storage)
        self.__session_repo = SessionRepository(self.session_storage)

    def get_user_repo(self) -> UserRepository:
        return self.__user_repo

    def get_lang_repo(self) -> LanguageRepository:
        return self.__lang_repo

    def get_session_repo(self) -> SessionRepository:
        return self.__session_repo

    def get_word_repo(self) -> WordRepository:
        return self.__word_repo
