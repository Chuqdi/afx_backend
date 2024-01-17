from datetime import datetime
from beanie import Link
from src.models.subscription import Subscription
from src.models.time_base_model import TimeBaseModel

from src.models.enums import TransactionType
from src.models.user import User


class BillingHistory(TimeBaseModel):
    user: Link[User]
    amount: int = 0
    transaction_type: TransactionType
    subscription_plan: str  # This could be PAYG, Starter plan, etc. It's highly dynamic based on what is set on stripe as price name.
    start_date: datetime = datetime.now()
    end_date: datetime
    subscription: Link[Subscription]

    class Settings:
        name = "billing_history"
        projection = {
            "user": "$user._id",
            "amount": 1,
            "transaction_type": 1,
            "subscription_plan": 1,
            "start_date": 1,
            "end_date": 1,
            "created_at": 1,
            "updated_at": 1,
            "subscription": 1,
        }
