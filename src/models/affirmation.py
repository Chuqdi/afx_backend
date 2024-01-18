from datetime import datetime
from src.models.affirmation_background_sound import AffirmationBackgroundSound
from src.models.affirmation_package import AffirmationPackage
from src.models.affirmation_voice import AffirmationVoice
from src.models.enums import AffirmationState, AffirmationType
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link

from src.models.user import User


class Affirmation(TimeBaseModel):
    user: Optional[Link[User]] = None
    title: str
    type: Optional[AffirmationType] = None
    package: Optional[Link[AffirmationPackage]] = None
    sentences: list[str]
    hours: int = 0
    last_listened_at: datetime
    starred: bool = False
    state: Optional[AffirmationState] = AffirmationState.NEW
    voice_id: Optional[Link[AffirmationVoice]] = None
    background_sound_id: Optional[Link[AffirmationBackgroundSound]] = None
    

    class Settings:
        name = "affirmation"
