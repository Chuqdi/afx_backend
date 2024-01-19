from fastapi import APIRouter, Depends
from src.models.user import User, UserUpdateInput
from src.utils.auth import verify_token
from src.utils.logger import get_logger
from src.utils.response import success_response

router = APIRouter()
logger = get_logger("MAIN")


@router.put("/")
async def update_user(payload: UserUpdateInput, user: User = Depends(verify_token)):
    await user.setValue(dict(payload))

    return success_response(
        data=None,
        message="User information updated successfully",
    )


@router.get(
    "/",
    response_model=User,
    response_model_exclude={
        "cognito_user_data",
        "revision_id",
        "id",
    },
)
async def get_user(current_user: User = Depends(verify_token)):
    return current_user
