from src.models.enums import ActorAccent
from src.models.time_base_model import TimeBaseModel
from typing import Optional


class AffirmationVoice(TimeBaseModel):
    audio_url: str
    accent: Optional[ActorAccent] = None
    actor_name: str

    class Settings:
        name = "affirmation_voice"

    class Config:
        json_schema_extra = {
            "example": {
                "audio_url": "https://download.samplelib.com/mp3/sample-15s.mp3",
                "accent": ActorAccent.AMERICAN.value,
                "actor_name": "John Wick",
            }
        }
