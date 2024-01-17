import typing
from src.models.affirmation import Affirmation
from src.models.affirmation_package_field import AffirmationPackageField
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link


class UserAffirmationPackageField(TimeBaseModel):
    affirmation: Optional[Affirmation] = None
    affirmation_package_field: Optional[Link[AffirmationPackageField]] = None
    value: typing.Any

    class Settings:
        name = "user_affirmation_package_field"
