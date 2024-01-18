from src.models.time_base_model import TimeBaseModel


class AffirmationBackgroundSound(TimeBaseModel):
    audio_url: str

    class Settings:
        name = "affirmation_background_sound"

    class Config:
        json_schema_extra = {
            "example": {
                "audio_url": "https://download.samplelib.com/mp3/sample-15s.mp3"
            }
        }
