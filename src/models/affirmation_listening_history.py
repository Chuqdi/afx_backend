from src.models.affirmation import Affirmation
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link
from datetime import datetime
from src.models.user import User


class AffirmationListeningHistory(TimeBaseModel):
    user: Optional[Link[User]] = None
    affirmation: Optional[Affirmation] = None
    start_at: datetime
    resumed_at: datetime
    listened_until: datetime
    completed: bool = False

    class Settings:
        name = "affirmation_listening_history"
