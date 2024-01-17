from typing import Literal, Optional
from beanie import Link
from src.models.stripe import StripePrice, StripeProduct
from src.models.time_base_model import TimeBaseModel
from src.models.user import User


class Subscription(TimeBaseModel):
    user: Link[User]
    product: Optional[Link[StripeProduct]] = None
    price: Optional[Link[StripePrice]] = None
    stripe_subscription_data: Optional[dict] = None
    billing_frequency: Literal["month", "year"]
    active: bool = False

    class Settings:
        name = "subscription"
