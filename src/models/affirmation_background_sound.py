from src.models.time_base_model import TimeBaseModel


class AffirmationBackgroundSound(TimeBaseModel):
    audio_url: str

    class Settings:
        name = "affirmation_background_sound"
