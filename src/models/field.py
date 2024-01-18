from typing import Optional
from src.models.enums import DataType
from src.models.time_base_model import TimeBaseModel


class Field(TimeBaseModel):
    key: str
    data_type: Optional[DataType] = None

    class Settings:
        name = "field"

    class Config:
        json_schema_extra = {"example": {"key": "text-field", "data_type": "string"}}
