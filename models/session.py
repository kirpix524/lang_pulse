import time
from datetime import datetime
import random
from utils.utils import parse_datetime
from models.dictionary import Dictionary, Word


class Session:
    def __init__(self, dictionary: Dictionary, session_id: int, words: list[Word]):
        self.__dictionary = dictionary
        self.__session_id = session_id
        self.__words = words
        self.__created_at = datetime.now()
        self.__last_repeated_at = None
        self.__direction = None
        self.__interval = None

        self.__active_words = []  # список слов в текущей тренировке
        self.__current_word = None
        self.__stats: list[dict] = []

    # Тренировка
    def start_training(self, direction: str, interval: float):
        self.__direction = direction
        self.__interval = interval
        self.__active_words = self.__words.copy()
        random.shuffle(self.__active_words)
        self.__current_word = None
        self.__last_repeated_at = datetime.now()

    def get_next_word(self) -> Word | None:
        if not self.__active_words:
            self.__current_word = None
            return None
        self.__current_word = self.__active_words[0]
        return self.__current_word

    def fix_stats(self, word, success: bool):
        if word:
            elapsed = time.time() - word.get_start_time()
            if success:
                recall_time = round(elapsed, 2)
            else:
                recall_time = None
            stats_row = {
                "word": word.word,
                "translation": word.translation,
                "success": success,
                "recall_time": recall_time,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "direction": self.__direction
            }
            self.__stats.append(stats_row)

    def mark_remembered(self):
        word= self.__current_word
        self.fix_stats(word, True)
        if self.__current_word in self.__active_words:
            self.__active_words.remove(self.__current_word)
        self.__current_word = None

    def mark_forgotten(self):
        self.fix_stats(self.__current_word, False)
        if self.__current_word in self.__active_words:
            self.__active_words.remove(self.__current_word)
            insert_pos = 3 + random.randint(0, 2)
            insert_pos = min(insert_pos, len(self.__active_words))  # чтобы не выйти за пределы
            self.__active_words.insert(insert_pos, self.__current_word)
        self.__current_word = None

    def pop_word(self):
        self.fix_stats(self.__current_word, True)
        if self.__current_word in self.__active_words:
            self.__active_words.remove(self.__current_word)
        self.__current_word = None

    def is_complete(self) -> bool:
        return len(self.__active_words) == 0

    def get_current_word(self) -> Word | None:
        return self.__current_word

    def init_word_tracking(self):
        if self.__current_word:
            self.__current_word.set_start_time(time.time())

    def get_stats(self) -> list[dict]:
        return self.__stats

    def add_words(self, words: list[Word]):
        for word in words:
            self.__words.append(word)

    def del_words(self, words: list[Word]):
        for word in words:
            self.__words.remove(word)

    def get_words(self) -> list[Word]:
        return self.__words

    def get_id(self):
        return self.__session_id

    def get_session_name(self):
        return f"Session {self.__session_id}"

    def get_user(self):
        return self.__dictionary.get_user()

    def get_language(self):
        return self.__dictionary.get_language()

    def set_created_at(self, created_at):
        self.__created_at = created_at

    def get_created_at(self):
        return parse_datetime(self.__created_at)

    def set_last_repeated_at(self, last_repeated_at):
        self.__last_repeated_at = last_repeated_at

    def get_last_repeated_at(self):
        return parse_datetime(self.__last_repeated_at)

    def get_words_not_in_session(self) -> list[Word]:
        existing_words = {w.word for w in self.__words}
        return [w for w in self.__dictionary.get_words() if w.word not in existing_words]

    def set_direction(self, direction):
        self.__direction = direction

    def get_direction(self):
        return self.__direction

    def set_interval(self, interval: float):
        self.__interval = interval

    def get_interval(self):
        return self.__interval