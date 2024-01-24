from src.models.affirmation import Affirmation
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link
from datetime import datetime
from src.models.user import User


class AffirmationListeningHistory(TimeBaseModel):
    user: Optional[Link[User]] = None
    affirmation: Optional[Link[Affirmation]] = None
    start_at: datetime
    resumed_at: datetime
    listened_until: datetime

    class Settings:
        name = "affirmation_listening_history"
        projection = {
            "user": "$user._id",
            "affirmation": "$affirmation._id",
            "resumed_at": 1,
            "listened_until": 1,
        }

    class Config:
        json_schema_extra = {
            "example": {
                "start_at": datetime.now(),
                "resumed_at": datetime.now(),
                "listened_until": datetime.now()
            }
        }
