from datetime import datetime

from src.models.enums import AffirmationState, AffirmationType
from src.models.time_base_model import TimeBaseModel
from typing import List, Optional
from beanie import Link

from src.models.user import User


class Affirmation(TimeBaseModel):
    user: Optional[Link[User]] = None
    type: Optional[AffirmationType] = None
    package: Optional[dict] = None
    state: Optional[AffirmationState] = AffirmationState.NEW
    sentences: Optional[List[str]] = None
    audio_url: Optional[str] = None
    total_seconds_listened: int = 0
    last_listened_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    starred: bool = False

    class Settings:
        name = "affirmation"
        projection = {
            "user": "$user._id",
            "type": 1,
            "package": 1,
            "state": 1,
            "audio_url": 1,
            "sentences": 1,
            "total_seconds_listened": 1,
            "last_listened_at": 1,
            "completed_at": 1,
            "starred": 1,
            "created_at": 1,
            "updated_at": 1,
        }

    class Config:
        json_schema_extra = {
            "example": {
                "type": AffirmationType.IAM.value,
                "package": {},
            }
        }
