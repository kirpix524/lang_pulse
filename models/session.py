import time
from datetime import datetime
import random
from utils.utils import parse_datetime
from models.dictionary import Dictionary, Word
from stats.stats import StatsRow
from storage.config import TrainingDirection

class Training:
    def __init__(self, direction: TrainingDirection, interval: float, words: list[Word], training_id: int, session_id: int):
        self.__direction = direction
        self.__interval = interval
        self.__training_date_time = datetime.now()
        self.__training_id = training_id
        self.__session_id = session_id

        self.__active_words = words.copy()
        random.shuffle(self.__active_words)
        self.__current_word = None
        self.__stats: list[StatsRow] = []

    def get_direction(self):
        return self.__direction

    def get_direction_value(self):
        return self.__direction.value if self.__direction else ''

    def set_direction(self, direction: TrainingDirection):
        self.__direction = direction

    def get_interval(self):
        return self.__interval

    def set_interval(self, interval):
        self.__interval = interval

    def get_training_date_time(self):
        return self.__training_date_time

    def set_training_date_time(self, training_date_time):
        self.__training_date_time = training_date_time

    def get_id(self):
        return self.__training_id

    def get_next_word(self) -> Word | None:
        if not self.__active_words:
            self.__current_word = None
            return None
        self.__current_word = self.__active_words[0]
        return self.__current_word

    def mark_remembered(self):
        word = self.__current_word
        self.__fix_stats(word, True, self.__session_id ,self.__training_id)
        if word in self.__active_words:
            self.__active_words.remove(word)
        self.__current_word = None

    def mark_forgotten(self):
        word = self.__current_word
        self.__fix_stats(word, False, self.__session_id ,self.__training_id)
        if word in self.__active_words:
            self.__active_words.remove(word)
            insert_pos = 3 + random.randint(0, 2)
            insert_pos = min(insert_pos, len(self.__active_words))
            self.__active_words.insert(insert_pos, word)
        self.__current_word = None

    def pop_word(self):
        self.__fix_stats(self.__current_word, True, self.__session_id ,self.__training_id)
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

    def get_stats(self) -> list[StatsRow]:
        return self.__stats

    def __fix_stats(self, word: Word, success: bool, session_id: int, training_id: int):
        if not word:
            return

        elapsed = time.time() - word.get_start_time() if success else None

        stat = StatsRow(
            word=word.word,
            translation=word.translation,
            session_id=session_id,
            training_id=training_id,
            success=success,
            recall_time=round(elapsed, 2) if elapsed is not None else None,
            timestamp=datetime.now().isoformat(timespec="seconds"),
            direction=self.__direction
        )

        self.__stats.append(stat)


class Session:
    def __init__(self, dictionary: Dictionary, session_id: int, words: list[Word]):
        self.__dictionary = dictionary
        self.__session_id = session_id
        self.__words = words
        self.__created_at = datetime.now()
        self.__last_repeated_at = None
        self.__trainings: list[Training] = []

        self.__current_training = None

    def add_new_training(self, direction: TrainingDirection, interval: float):
        new_training_id = 1 if not self.__trainings else self.__trainings[-1].get_id() + 1
        training = Training(direction, interval, self.__words.copy(), new_training_id, self.__session_id)
        self.__current_training = training
        self.__trainings.append(training)
        self.__last_repeated_at = training.get_training_date_time()

    def add_existing_training(self, direction: TrainingDirection, interval: float, training_id: int = None, training_date_time = None):
        training = Training(direction, interval, [], training_id, self.__session_id)
        training.set_training_date_time(training_date_time)
        self.__trainings.append(training)

    def get_current_training(self):
        return self.__current_training

    def get_trainings(self) -> list[Training]:
        return self.__trainings

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

    def can_be_changed(self) -> bool:
        return not self.__trainings

    def get_total_trainings(self) -> int:
        return len(self.__trainings)