import stripe
from beanie import PydanticObjectId
from fastapi import HTTPException
from src.config import STRIPE_SECRET_KEY

from src.models.payment import UserPaymentMethod
from src.models.stripe import StripeCharge
from src.models.user import User

# Initialize the Stripe library
stripe.api_key = STRIPE_SECRET_KEY


def stripe_client():
    return stripe


def charge_card(input: StripeCharge):
    stripe = stripe_client()
    # Charge the card using the Stripe API
    charge = stripe.Charge.create(
        amount=input.amount,
        currency=input.currency,
        source=input.token,  # Tokenized card information
        description=input.description,
    )

    # Check if the charge was successful
    if charge.status == "succeeded":
        return 200

    return 400


async def create_or_fetch_stripe_customer(user_id: str):
    """
    Create a new Stripe customer.

    This function creates a new Stripe customer and assigns the `stripe_customer_id` to the user dict.
    If the user already has a `stripe_customer_id`, returns it.

    :param user_id: The ID of the user.
    :type user_id: str

    :return: Stripe customer id.
    :rtype: dict
    """

    user = await User.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.stripe_customer_id:
        return user.stripe_customer_id

    stripe = stripe_client()
    # Create a customer in Stripe
    customer = stripe.Customer.create(
        email=user.email,
        description="Customer for {}".format(user.email),
    )

    # Update the user's stripe customer id
    await user.set({"stripe_customer_id": customer.id})

    return customer.id


async def check_payment_method_for_availability(
    user_id: PydanticObjectId, finger_print: str
):
    """
    Check user's payment methods for availability

    Here, we check if the card has already been added to the platform before now
    by the user

    :param user_id: The ID of the user.
    :type user_id: PydanticObjectId

    :param finger_print: Unique identifier for card numbers
    :type finger_print: str

    :return boolean
    """

    user = await User.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    paymentMethod = await UserPaymentMethod.find_one(
        {
            "user.sub_id": user.sub_id,
            "data.card.fingerprint": finger_print,
        },
        fetch_links=True,
    )

    if paymentMethod == None:
        return True

    return False
