from beanie import PydanticObjectId
from fastapi import HTTPException
from src.models.credit_history import CreditHistory
from src.models.enums import (
    CampaignType,
    CreditTransactionSource,
    CreditTransactionType,
)
from src.models.user import User
from src.utils.internal_configuration import get_current_internal_configuration


async def remove_user_credit(
    user_id: PydanticObjectId,
    amount: int,
    source=None,
    source_id=None,
):
    """
    Deduct a specified amount of credits from a user's account.

    Parameters:
    - user_id (PydanticObjectId): The ID of the user from whom credits will be deducted.
    - amount (int): The amount of credits to deduct from the user's account.

    Raises:
    - HTTPException(404): If the user with the provided user_id is not found.
    - HTTPException(400): If the user has insufficient available credit to deduct
                          the specified amount.

    Returns:
    - User: The updated user object with the deducted credits if the operation is successful.

    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.credits >= amount:
        await user.set({"credits": user.credits - amount})

        # Create Credit Transaction
        credit_transaction = CreditHistory(
            user=user.dict(),
            amount=amount,
            transaction_type=CreditTransactionType.DEBIT,
            source=source if source else CreditTransactionSource.CAMPAIGN,
            source_id=source_id if source_id else user_id,
        )
        await credit_transaction.insert()  # type: ignore
    else:
        raise HTTPException(status_code=404, detail="Insufficient Available Credit")
    return user


async def add_user_credit(
    user_id: PydanticObjectId,
    amount: int,
    source=CreditTransactionSource.CAMPAIGN,
    source_id=None,
):
    """
    Add a specified amount of credits to a user's account.

    Parameters:
    - user_id (PydanticObjectId): The ID of the user to whom credits will be added.
    - amount (int): The amount of credits to add to the user's account.
    - source (enum): The trigger of the add credit operation

    Raises:
    - HTTPException(404): If the user with the provided user_id is not found.

    Returns:
    - User: The updated user object with the added credits if the operation is successful.

    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.set({"credits": user.credits + amount})

    # Create Credit Transaction
    credit_transaction = CreditHistory(
        user=user.dict(),
        amount=amount,
        transaction_type=CreditTransactionType.CREDIT,
        source=source,
        source_id=source_id if source_id else user_id,
    )
    await credit_transaction.create()
    return user


async def compute_budget(campaign_type: CampaignType, mention_purchased: int):
    """
    Compute budget amount based on campaign type and the mentions purchased

    Parameters:
    - campaign_type (CampaignType): The type of the campaign
    - mention_purchased (int): The amount of credits to add to the user's account.

    Returns:
    - credits(int): The calculated budget in credits
    """
    current_internal_configuration = await get_current_internal_configuration()
    if campaign_type == CampaignType.FLOODING:
        credits = (
            mention_purchased
            / current_internal_configuration.credit_per_flooding_mention
        )
    else:
        credits = (
            mention_purchased
            / current_internal_configuration.credit_per_organic_mention
        )
    return credits
