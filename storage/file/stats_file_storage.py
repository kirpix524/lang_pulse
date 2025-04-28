from datetime import datetime
from pathlib import Path

from app.config import TrainingDirection
from models.user_dictionary import UserDictionary
from models.language import Language
from models.session import Session, Training
from models.stats import StatsRow
from models.user import User
from storage.interfaces import IStatsStorage


class StatsFileStorage(IStatsStorage):
    def __init__(self, stats_data: dict[str, str]):
        self.__stats_data = stats_data

    def __get_stats_file_name(self, user: User, language: Language) -> str:
        file_path = (f"{self.__stats_data['DIRECTORY']}"
                     + f"{self.__stats_data['FILE_NAME_PREFIX']}_{user.username}_{language.lang_code}.txt")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def save_training_stats(self, session: Session, training: Training):
        """
        Сохраняет статистику тренировки в файл.
        """
        stats = training.get_stats()
        file_path = self.__get_stats_file_name(session.get_user(), session.get_language())

        with open(file_path, "a", encoding="utf-8") as f:
            for stat in stats:
                line = "T|" + "|".join([
                    str(stat.session_id),
                    str(stat.training_id),
                    str(stat.term),
                    str(stat.translation),
                    "1" if stat.success else "0",
                    f"{stat.recall_time:.2f}" if stat.recall_time is not None else "",
                    str(stat.timestamp),
                    stat.get_direction_value()
                ])
                f.write(line + "\n")

    def load_training_stats_words(self, user: User, language: Language, dictionary: UserDictionary):
        def parse_direction(value: str) -> TrainingDirection | None:
            try:
                return TrainingDirection(value)
            except ValueError:
                return None  # или выбросить исключение, если нужно строго

        file_path = self.__get_stats_file_name(user, language)
        words = dictionary.get_words()
        word_keys = {(w.word.term, w.word.translation) for w in words}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("T|"):
                        continue
                    parts = line.strip().split("|")
                    if len(parts) < 8:
                        continue
                    # гарантируем, что будет 9 элементов
                    _, session_id, training_id, word, translation, success, recall_time, timestamp, direction = (parts + [""] * 9)[:9]

                    if (word, translation) not in word_keys:
                        continue

                    word_obj = dictionary.find_word(word, translation)
                    if not word_obj:
                        continue

                    stat = StatsRow(
                        term=word,
                        translation=translation,
                        session_id=int(session_id),
                        training_id=int(training_id),
                        success=(success == "1"),
                        recall_time=float(recall_time) if recall_time else None,
                        timestamp=datetime.fromisoformat(timestamp) if timestamp else None,
                        direction=parse_direction(direction)
                    )

                    word_obj.add_stat(stat)

        except FileNotFoundError:
            print(f"Статистика не найдена: {file_path}")
