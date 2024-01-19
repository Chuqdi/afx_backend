from fastapi import APIRouter, Depends, status
from src.models.token import Token
from src.models.user import User, CognitoData
from src.utils.auth import authenticate_user
from src.utils.logger import get_logger
from src.utils.response import success_response
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
logger = get_logger("MAIN")


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = authenticate_user(form_data.username, form_data.password)
    return {
        "status": status.HTTP_200_OK,
        "access_token": tokens["access_token"],
        "token_type": "bearer",
    }


@router.post("/register")
async def register(data: CognitoData):
    """Register a new user User"""
    saved_user = User(
        email=data.cognito_data["user"]["username"],
        sub_id=data.cognito_data["userSub"],
        cognito_user_data=data.cognito_data,
    )
    await saved_user.create()  # type: ignore
    return success_response(
        saved_user, "User created successfully, Check email to verify account", 201
    )
