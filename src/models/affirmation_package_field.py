from src.models.affirmation_package import AffirmationPackage
from src.models.field import Field
from src.models.time_base_model import TimeBaseModel
from typing import Optional
from beanie import Link


class AffirmationPackageField(TimeBaseModel):
    field: Optional[Link[Field]] = None
    affirmation_package: Optional[Link[AffirmationPackage]] = None
    required: bool = False

    class Settings:
        name = "affirmation_package_field"
