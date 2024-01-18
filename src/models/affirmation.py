from datetime import datetime
from src.models.enums import AffirmationState, AffirmationType
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link

from src.models.user import User


class Affirmation(TimeBaseModel):
    user: Optional[Link[User]] = None
    type: Optional[AffirmationType] = None
    package: Optional[dict] = None
    state: Optional[AffirmationState] = AffirmationState.NEW
    sentences: Optional[str] = None
    hours: int = 0
    last_listened_at: Optional[datetime] = None
    starred: bool = False

    class Settings:
        name = "affirmation"

    class Config:
        json_schema_extra = {
            "example": {
                "type": AffirmationType.IAM.value,
                "package": {},
            }
        }
