from typing import Optional
from src.models.enums import DataType
from src.models.time_base_model import TimeBaseModel


class Field(TimeBaseModel):
    key: str
    data_type: Optional[DataType] = None
    required: bool = False

    class Settings:
        name = "field"
