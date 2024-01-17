from src.models.affirmation_background_sound import AffirmationBackgroundSound
from src.models.affirmation_voice import AffirmationVoice
from src.models.time_base_model import TimeBaseModel
from typing import List


class AffirmationPackage(TimeBaseModel):
    title: str
    subtitle: str
    image_url: str
    goals: List[dict]
    limiting_beliefs: List[str]
    affirmation_voices: List[AffirmationVoice]
    affirmation_background_sounds: List[AffirmationBackgroundSound]

    class Settings:
        name = "affirmation_package"
