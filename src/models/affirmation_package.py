from beanie import Link
from pydantic import BaseModel
from src.models.affirmation_background_sound import AffirmationBackgroundSound
from src.models.affirmation_voice import AffirmationVoice
from src.models.time_base_model import TimeBaseModel
from typing import List


class Goal(BaseModel):
    title: str
    description: str


class AffirmationPackage(TimeBaseModel):
    title: str
    subtitle: str
    image_url: str
    goals: List[Goal]
    limiting_beliefs: List[str]
    affirmation_voices: List[Link[AffirmationVoice]]
    affirmation_background_sounds: List[Link[AffirmationBackgroundSound]]

    class Settings:
        name = "affirmation_package"


class AffirmationPackageInput(BaseModel):
    title: str
    subtitle: str
    image_url: str
    goals: List[Goal]
    limiting_beliefs: List[str]
    affirmation_voices: List[str]
    affirmation_background_sounds: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Ecommerce",
                "subtitle": "This is a subtitle",
                "image_url": "https://cdn.pixabay.com/photo/2024/01/04/14/27/write-8487618_640.jpg",
                "goals": [
                    {
                        "title": "Awareness",
                        "description": "Get people to know my brand",
                    },
                    {
                        "title": "Investors",
                        "description": "Get interested investors for my brand",
                    },
                    {
                        "title": "Market",
                        "description": "Get a impactful share of the market",
                    },
                ],
                "limiting_beliefs": [
                    "LimitingBelief 1",
                    "LimitingBelief 2",
                    "LimitingBelief 3",
                ],
                "affirmation_voices": ["uuid"],
                "affirmation_background_sounds": ["uuid"],
            }
        }
