from src.models.enums import ActorAccent
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link

from src.models.user import User


class AffirmationVoice(TimeBaseModel):
    user: Optional[Link[User]] = None
    audio_url: str
    accent: Optional[ActorAccent] = None
    actor_name: str

    class Settings:
        name = "affirmation_voice"
