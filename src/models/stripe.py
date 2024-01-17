from typing import Literal, Optional
from beanie import Link
from pydantic import BaseModel
from src.models.time_base_model import TimeBaseModel
from src.models.enums import PaymentFrequency


class StripePaymentIntent(BaseModel):
    amount: int | float
    currency: str
    payment_method: str
    payment_frequency: PaymentFrequency
    card_tokenization_id: str
    promo_code: Optional[str] = None


class StripeCharge(BaseModel):
    amount: int
    currency: str
    token: str
    description: str


class StripeSubscription(BaseModel):
    product_id: str
    billing_frequency: Literal["month", "year"]
    default_payment_method: str

    class Config:
        json_schema_extra = {
            "example": {"product_id": "1", "billing_frequency": "year or month"}
        }


class StripePrice(TimeBaseModel):
    unit_amount: int  # in usd
    credits: int
    currency: str
    billing_frequency: Literal["month", "year"]
    stripe_price: Optional[dict] = None

    class Settings:
        name = "stripe_price"

    class Config:
        json_schema_extra = {
            "example": {
                "unit_amount": 1000,
                "credits": 5000,
                "currency": "usd",
                "billing_frequency": "month | year",
            }
        }


class StripeProduct(TimeBaseModel):
    name: str
    description: str
    discount: int = 0
    stripe_product: Optional[dict] = None

    month_price_id: Optional[Link[StripePrice]] = None
    year_price_id: Optional[Link[StripePrice]] = None

    highlighted: Optional[bool] = False
    options: Optional[list[str]] = None

    active: bool = False

    class Settings:
        name = "stripe_product"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Starter plan",
                "description": "Basic plan for the ",
                "month_price_id": "Enter the price id for a month subscription",
                "year_price_id": "Enter the price id for a year subscription",
                "discount": "Specify the amount of discount from 1, 100. The user gets when actively on this subscription",
                "options": [
                    "Run Continuous Campaigns!",
                    "Get 20% off for all additional Credits!",
                ],
            }
        }
