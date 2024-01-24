from typing import Optional
from beanie import Indexed
from pydantic import BaseModel
from src.models.enums import (
    AffirmationExperienceLevel,
    RelationshipStatus,
    UserGender,
    UserRole,
)
from src.models.time_base_model import TimeBaseModel
from datetime import datetime


class User(TimeBaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Indexed(str, unique=True)  # type: ignore
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    suspended: bool = False
    sub_id: Optional[str] = None
    role: Optional[UserRole] = UserRole.REGULAR
    gender: Optional[UserGender] = None
    cognito_user_data: dict
    stripe_customer_id: Optional[str] = None
    dob: Optional[datetime] = None
    relationship_status: Optional[RelationshipStatus] = None
    onboarding_completed: bool = False
    explainer_completed: bool = False
    affirmation_experience_level: Optional[AffirmationExperienceLevel] = None
    credits: int = 0
    is_marked_for_deletion: bool = False

    class Settings:
        name = "user"


class CognitoData(BaseModel):
    cognito_data: dict

    class Config:
        json_schema_extra = {
            "example": {
                "data": dict(),
            }
        }


class UserUpdateInput(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[UserGender] = None
    dob: Optional[datetime] = None
    relationship_status: Optional[RelationshipStatus] = None
    onboarding_completed: Optional[bool] = False
    explainer_completed: Optional[bool] = False
    affirmation_experience_level: Optional[AffirmationExperienceLevel] = None
