from typing import Optional
from beanie import Indexed
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
    sub_id: str
    role: Optional[UserRole] = UserRole.REGULAR
    gender: Optional[UserGender] = None
    cognito_user_data: dict
    stripe_customer_id: Optional[str] = None
    dob: datetime
    relationship_status: Optional[RelationshipStatus] = None
    onboarding_completed: bool = False
    affirmation_experience_level: Optional[AffirmationExperienceLevel] = None
    credits: int = 0
    is_marked_for_deletion: bool = False

    class Settings:
        name = "user"
