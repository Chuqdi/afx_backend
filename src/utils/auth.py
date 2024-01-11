import boto3
from fastapi import Depends, HTTPException
from src.config import COGNITO_CLIENT_ID, COGNITO_REGION
from src.models.enums import UserRole
from src.models.user import User
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
client = boto3.client("cognito-idp", region_name=COGNITO_REGION)


# Function to verify JWT tokens
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        response = client.get_user(AccessToken=token)
        # Token is valid, you can access user information in response['UserAttributes']
        sub_id = response["UserAttributes"][0]["Value"]
        user = await User.find_one(User.sub_id == sub_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except client.exceptions.NotAuthorizedException:
        # Token is not valid
        return None
    except client.exceptions.UserNotFoundException:
        # User not found
        return None


async def verify_admin_token(token: str = Depends(oauth2_scheme)):
    try:
        response = client.get_user(AccessToken=token)
        # Token is valid, you can access user information in response['UserAttributes']
        sub_id = response["UserAttributes"][0]["Value"]
        user = await User.find_one(User.sub_id == sub_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        if user.role is not UserRole.ADMIN:
            raise HTTPException(
                status_code=403, detail="Forbidden: Only Admin can access this resource"
            )

        return user
    except client.exceptions.NotAuthorizedException:
        # Token is not valid
        return None
    except client.exceptions.UserNotFoundException:
        # User not found
        return None


def authenticate_user(username, password):
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientId=COGNITO_CLIENT_ID,
        )

        if "AuthenticationResult" in response:
            return {
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                "id_token": response["AuthenticationResult"]["IdToken"],
            }
        else:
            return {"error": "Authentication failed"}

    except Exception as e:
        return {"error": str(e)}
