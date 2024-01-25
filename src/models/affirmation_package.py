from src.models.time_base_model import TimeBaseModel
from typing import List, Optional


class AffirmationPackage(TimeBaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    category: dict
    sentences: Optional[List[str]] = None
    image_url: Optional[str] = None
    credits: int = 1
    form: List[dict]
    answers: List[dict]

    class Settings:
        name = "affirmation_package"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Ecommerce",
                "subtitle": "This is a subtitle",
                "description": "This is a description",
                "category": {},
                "sentences": [],
                "image_url": "http://website.com",
                "credits": 1,
                "form": {},
                "answers": {},
            }
        }
