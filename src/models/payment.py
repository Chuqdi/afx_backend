from typing import Optional
from beanie import Link
from src.models.time_base_model import TimeBaseModel
from src.models.enums import PaymentMethodType
from src.models.user import User


class UserPaymentMethod(TimeBaseModel):
    user: Optional[Link[User]] = None
    type: PaymentMethodType = PaymentMethodType.CARD
    data: dict
    is_default: bool = False

    class Settings:
        name = "user_payment_method"
        projection = {
            "type": 1,
            "user": "$user._id",
            "created_at": 1,
            "updated_at": 1,
            "data": 1,
            "is_default": 1,
        }


class UsedPaymentIntent(TimeBaseModel):
    """Used stripe's payment intent
    - This model will hold all payment intents that has been used within the platform
    - Payment intents are used if a user wants to topup or subscribe while being charged for initial payment
    """

    intent_id: str
    success: bool = True
    user: Optional[Link[User]] = None

    class Settings:
        name = "used_payment_intent"
