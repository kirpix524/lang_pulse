from abc import ABC, abstractmethod
import time
from datetime import datetime
import random
from models.user_word import IBasicUserWord
from models.language import Language
from models.user import User
from models.stats import StatsRow
from app.config import TrainingDirection

class WordHandlingStrategy(ABC):
    @abstractmethod
    def handle_remembered(self, training: 'Training', word: IBasicUserWord) -> None:
        pass

    @abstractmethod
    def handle_forgotten(self, training: 'Training', word: IBasicUserWord) -> None:
        pass

    @abstractmethod
    def handle_pop_word(self, training: 'Training', word: IBasicUserWord) -> None:
        pass

class DefaultWordHandlingStrategy(WordHandlingStrategy):
    def handle_remembered(self, training: 'Training', word: IBasicUserWord):
        training._fix_stats(word, True)
        if word in training._active_words:
            training._active_words.remove(word)
        training._current_word = None

    def handle_forgotten(self, training: 'Training', word: IBasicUserWord):
        training._fix_stats(word, False)
        if word in training._active_words:
            training._active_words.remove(word)
            insert_pos = 3 + random.randint(0, 2)
            insert_pos = min(insert_pos, len(training._active_words))
            training._active_words.insert(insert_pos, word)
        training._current_word = None

    def handle_pop_word(self, training: 'Training', word: IBasicUserWord):
        training._fix_stats(word, True)
        if word in training._active_words:
            training._active_words.remove(word)
        training._current_word = None

class Training:
    def __init__(self,
                 direction: TrainingDirection,
                 interval: float,
                 words: list[IBasicUserWord],
                 training_id: int,
                 session_id: int,
                 strategy: WordHandlingStrategy = DefaultWordHandlingStrategy(),
                 need_shuffle: bool = True):
        self.interval: float = interval
        self.direction: TrainingDirection = direction
        self.__training_date_time: datetime = datetime.now()
        self.__training_id: int = training_id
        self.__session_id: int = session_id

        self._active_words: list[IBasicUserWord] = words.copy()
        if need_shuffle:
            random.shuffle(self._active_words)
        self.__current_word: IBasicUserWord | None = None
        self.__stats: list[StatsRow] = []
        self.__strategy: WordHandlingStrategy = strategy


    def get_direction_value(self) -> str:
        return self.direction.value if self.direction else ''

    @property
    def training_date_time(self) -> datetime:
        return self.__training_date_time

    @training_date_time.setter
    def training_date_time(self, value: datetime):
        self.__training_date_time = value

    def get_id(self) -> int:
        return self.__training_id

    def get_next_word(self) -> IBasicUserWord | None:
        if not self._active_words:
            self.__current_word = None
            return None
        self.__current_word = self._active_words[0]
        return self.__current_word

    def mark_remembered(self) -> None:
        if self.__current_word:
            self.__strategy.handle_remembered(self, self.__current_word)

    def mark_forgotten(self) -> None:
        if self.__current_word:
            self.__strategy.handle_forgotten(self, self.__current_word)

    def pop_word(self) -> None:
        if self.__current_word:
            self.__strategy.handle_pop_word(self, self.__current_word)

    def is_complete(self) -> bool:
        return len(self._active_words) == 0

    def get_current_word(self) -> IBasicUserWord | None:
        return self.__current_word

    def init_word_tracking(self) -> None:
        if self.__current_word:
            self.__current_word.set_start_time(time.time())

    def get_stats(self) -> list[StatsRow]:
        return self.__stats

    def _fix_stats(self, word: IBasicUserWord, success: bool) -> None:
        if not word:
            return

        elapsed = time.time() - word.get_start_time() if success else None

        stat = StatsRow(
            term=word.word.term,
            translation=word.word.translation,
            session_id=self.__session_id,
            training_id=self.__training_id,
            success=success,
            recall_time=round(elapsed, 2) if elapsed is not None else None,
            timestamp=datetime.now(),
            direction=self.direction
        )

        self.__stats.append(stat)

class Session:
    def __init__(self, user: User, language: Language, session_id: int, words: list[IBasicUserWord]):
        self.__user = user
        self.__language = language
        self.__session_id = session_id
        self.__words = words
        self.__created_at = datetime.now()
        self.__last_repeated_at = None
        self.__trainings: list[Training] = []
        self.__current_training = None
        self.__session_name = ""

    def add_new_training(self, direction: TrainingDirection, interval: float) -> None:
        new_training_id = 1 if not self.__trainings else self.__trainings[-1].get_id() + 1
        training = Training(direction, interval, self.__words.copy(), new_training_id, self.__session_id)
        self.__current_training = training
        self.__trainings.append(training)
        self.__last_repeated_at = training.training_date_time

    def add_existing_training(self,
                              direction: TrainingDirection,
                              interval: float,
                              training_id: int = None,
                              training_date_time: datetime = None) -> None:
        training = Training(direction, interval, [], training_id, self.__session_id)
        training.training_date_time=training_date_time
        self.__trainings.append(training)

    def get_current_training(self) -> Training:
        return self.__current_training

    def get_trainings(self) -> list[Training]:
        return self.__trainings

    def add_words(self, words: list[IBasicUserWord]) -> None:
        for word in words:
            self.__words.append(word)

    def del_words(self, words: list[IBasicUserWord]) -> None:
        for word in words:
            self.__words.remove(word)

    def get_words(self) -> list[IBasicUserWord]:
        return self.__words

    def get_id(self) -> int:
        return self.__session_id

    def set_session_name(self, new_name: str) -> None:
        self.__session_name = new_name

    def get_session_name(self) -> str:
        return f"Session {self.__session_id}"

    def get_user(self) -> User:
        return self.__user

    def get_language(self) -> Language:
        return self.__language

    def set_created_at(self, created_at: datetime) -> None:
        self.__created_at = created_at

    def get_created_at(self) -> datetime:
        return self.__created_at

    def get_created_at_str(self, fmt: str = "%d.%m.%Y") -> str:
        created_at = self.get_created_at()
        if not created_at:
            return ''
        return self.__created_at.strftime(fmt)

    def get_last_repeated_at_str(self, fmt: str = "%d.%m.%Y") -> str:
        last_repeated_at = self.get_last_repeated_at()
        if not last_repeated_at:
            return ''
        return last_repeated_at.strftime(fmt)

    def get_last_repeated_at(self) -> datetime | None:
        if not self.__trainings:
            return None
        latest = max(self.__trainings, key=lambda t: t.training_date_time)
        return latest.training_date_time

    def can_be_changed(self) -> bool:
        return not self.__trainings

    def get_total_trainings(self) -> int:
        return len(self.__trainings)