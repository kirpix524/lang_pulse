from datetime import datetime
from app.config import TrainingDirection, get_direction_name

class StatsRow:
    def __init__(
        self,
        word: str,
        translation: str,
        session_id: int,
        training_id: int,
        success: bool,
        recall_time: float | None,
        timestamp: datetime,
        direction: TrainingDirection
    ):
        self.word = word
        self.translation = translation
        self.session_id = session_id
        self.training_id = training_id
        self.success = success
        self.recall_time = recall_time
        self.timestamp = timestamp  # теперь это datetime
        self.direction = direction

    def get_direction_value(self) -> str:
        return self.direction.value if self.direction else ""

    def get_direction_name(self) -> str:
        return get_direction_name(self.direction) if self.direction else ""

    def get_timestamp_str(self, fmt: str = "%d.%m.%Y") -> str:
        """
        Возвращает отформатированную строку даты/времени.
        По умолчанию: '17.04.2025 14:30'
        """
        if not self.timestamp:
            return ""
        return self.timestamp.strftime(fmt)
