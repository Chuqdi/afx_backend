from typing import Optional
from beanie import Link, PydanticObjectId
from src.models.time_base_model import TimeBaseModel

from src.models.enums import TransactionSource, TransactionType
from src.models.user import User


class UserCreditingSystem(TimeBaseModel):
    user: Link[User]
    amount: int = 0
    transaction_type: TransactionType
    source: TransactionSource
    source_id: PydanticObjectId
    amount_cash: Optional[float | int] = None

    class Settings:
        name = "user_crediting_system"
        projection = {
            "user": "$user._id",
            "amount": 1,
            "transaction_type": 1,
            "source": 1,
            "source_id": 1,
            "created_at": 1,
            "updated_at": 1,
            "amount_cash": 1,
        }
