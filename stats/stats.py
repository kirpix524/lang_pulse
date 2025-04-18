from datetime import datetime
from storage.config import TrainingDirection, get_direction_name

class StatsRow:
    def __init__(
        self,
        word: str,
        translation: str,
        session_id: int,
        training_id: int,
        success: bool,
        recall_time: float | None,
        timestamp: str,
        direction: TrainingDirection
    ):
        self.word = word
        self.translation = translation
        self.session_id = session_id
        self.training_id = training_id
        self.success = success
        self.recall_time = recall_time  # в секундах, None если не вспомнил
        self.timestamp = timestamp  # ISO строка '2025-04-17T13:55:00'
        self.direction = direction  # 'to_ru' или 'to_foreign'

    def to_dict(self) -> dict:
        return {
            "word": self.word,
            "translation": self.translation,
            "session_id": self.session_id,
            "training_id": self.training_id,
            "success": self.success,
            "recall_time": self.recall_time,
            "timestamp": self.timestamp,
            "direction": self.direction.value if self.direction else ''
        }

    @staticmethod
    def from_dict(data: dict) -> "StatsRow":
        return StatsRow(
            word=data.get("word", ""),
            translation=data.get("translation", ""),
            session_id=int(data.get("session_id", 0)),
            training_id=int(data.get("training_id", 0)),
            success=bool(data.get("success")),
            recall_time=float(data.get("recall_time")) if data.get("recall_time") not in (None, "") else None,
            timestamp=data.get("timestamp", datetime.now().isoformat(timespec="seconds")),
            direction=TrainingDirection(data.get("direction", "")) if data.get("direction") else None
        )

    def get_direction_value(self) -> str:
        if self.direction:
            return self.direction.value
        else:
            return ""

    def get_direction_name(self) -> str:
        if self.direction:
            return get_direction_name(self.direction)
        else:
            return ''
