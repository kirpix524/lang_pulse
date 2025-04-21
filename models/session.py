from abc import ABC, abstractmethod
import time
from datetime import datetime
import random
from utils.utils import parse_datetime
from models.dictionary import Dictionary, WordInterface
from stats.stats import StatsRow
from storage.config import TrainingDirection

class WordHandlingStrategy(ABC):
    @abstractmethod
    def handle_remembered(self, training: 'Training', word: WordInterface):
        pass

    @abstractmethod
    def handle_forgotten(self, training: 'Training', word: WordInterface):
        pass

    @abstractmethod
    def handle_pop_word(self, training: 'Training', word: WordInterface):
        pass

class DefaultWordHandlingStrategy(WordHandlingStrategy):
    def handle_remembered(self, training: 'Training', word: WordInterface):
        training._fix_stats(word, True)
        if word in training._active_words:
            training._active_words.remove(word)
        training._current_word = None

    def handle_forgotten(self, training: 'Training', word: WordInterface):
        training._fix_stats(word, False)
        if word in training._active_words:
            training._active_words.remove(word)
            insert_pos = 3 + random.randint(0, 2)
            insert_pos = min(insert_pos, len(training._active_words))
            training._active_words.insert(insert_pos, word)
        training._current_word = None

    def handle_pop_word(self, training: 'Training', word: WordInterface):
        training._fix_stats(word, True)
        if word in training._active_words:
            training._active_words.remove(word)
        training._current_word = None

class Training:
    def __init__(self,
                 direction: TrainingDirection,
                 interval: float,
                 words: list[WordInterface],
                 training_id: int,
                 session_id: int,
                 strategy: WordHandlingStrategy = DefaultWordHandlingStrategy(),
                 need_shuffle: bool = True):
        self.__direction = direction
        self.__interval = interval
        self.__training_date_time = datetime.now()
        self.__training_id = training_id
        self.__session_id = session_id

        self._active_words = words.copy()
        if need_shuffle:
            random.shuffle(self._active_words)
        self.__current_word = None
        self.__stats: list[StatsRow] = []
        self.__strategy = strategy


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

    def get_next_word(self) -> WordInterface | None:
        if not self._active_words:
            self.__current_word = None
            return None
        self.__current_word = self._active_words[0]
        return self.__current_word

    def mark_remembered(self):
        if self.__current_word:
            self.__strategy.handle_remembered(self, self.__current_word)

    def mark_forgotten(self):
        if self.__current_word:
            self.__strategy.handle_forgotten(self, self.__current_word)

    def pop_word(self):
        if self.__current_word:
            self.__strategy.handle_pop_word(self, self.__current_word)

    def is_complete(self) -> bool:
        return len(self._active_words) == 0

    def get_current_word(self) -> WordInterface | None:
        return self.__current_word

    def init_word_tracking(self):
        if self.__current_word:
            self.__current_word.set_start_time(time.time())

    def get_stats(self) -> list[StatsRow]:
        return self.__stats

    def _fix_stats(self, word: WordInterface, success: bool):
        if not word:
            return

        elapsed = time.time() - word.get_start_time() if success else None

        stat = StatsRow(
            word=word.word,
            translation=word.translation,
            session_id=self.__session_id,
            training_id=self.__training_id,
            success=success,
            recall_time=round(elapsed, 2) if elapsed is not None else None,
            timestamp=datetime.now().isoformat(timespec="seconds"),
            direction=self.__direction
        )

        self.__stats.append(stat)


class Session:
    def __init__(self, dictionary: Dictionary, session_id: int, words: list[WordInterface]):
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

    def add_words(self, words: list[WordInterface]):
        for word in words:
            self.__words.append(word)

    def del_words(self, words: list[WordInterface]):
        for word in words:
            self.__words.remove(word)

    def get_words(self) -> list[WordInterface]:
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

    def get_words_not_in_session(self) -> list[WordInterface]:
        existing_words = {w.word for w in self.__words}
        return [w for w in self.__dictionary.get_words() if w.word not in existing_words]

    def can_be_changed(self) -> bool:
        return not self.__trainings

    def get_total_trainings(self) -> int:
        return len(self.__trainings)