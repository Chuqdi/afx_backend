from src.models.affirmation import Affirmation
from src.models.time_base_model import TimeBaseModel
from typing import List, Optional
from beanie import Link
from src.models.user import User


class AffirmationStatistic(TimeBaseModel):
    user: Optional[Link[User]] = None
    year: str
    week: int = 1
    affirmations: Optional[List[Affirmation]] = None
    completed_days: Optional[List[str]] = None  # 1 = Monday ... 7 = Sunday
    listened_affirmation_hours: int = 0

    class Settings:
        name = "affirmation_statistic"
