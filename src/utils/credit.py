from beanie import PydanticObjectId
from fastapi import HTTPException
from src.models.user_crediting_system import UserCreditingSystem
from src.models.enums import (
    TransactionSource,
    TransactionType,
)
from src.models.user import User


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
        credit_transaction = UserCreditingSystem(
            user=user.dict(),
            amount=amount,
            transaction_type=TransactionType.DEBIT,
            source=source if source else TransactionSource.AFFIRMATION,
            source_id=source_id if source_id else user_id,
        )
        await credit_transaction.insert()  # type: ignore
    else:
        raise HTTPException(status_code=404, detail="Insufficient Available Credit")
    return user


async def add_user_credit(
    user_id: PydanticObjectId,
    amount: int,
    source=TransactionSource.AFFIRMATION,
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
    credit_transaction = UserCreditingSystem(
        user=user.dict(),
        amount=amount,
        transaction_type=TransactionType.CREDIT,
        source=source,
        source_id=source_id if source_id else user_id,
    )
    await credit_transaction.create()
    return user

