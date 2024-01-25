from fastapi import APIRouter, Depends, HTTPException
from src.models.user import User, UserUpdateInput
from src.utils.auth import verify_token
from src.utils.logger import get_logger
from src.utils.response import success_response
from src.utils.file_extensions import AllowedExtensions
from src.utils.logger import get_logger
from src.utils.response import success_response
from fastapi import File, UploadFile
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from boto3 import client as boto3_client
from src.utils.image_upload import resize_image
from datetime import datetime


router = APIRouter()
logger = get_logger("MAIN")

from src.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    COGNITO_REGION,
)


ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]

s3_client = boto3_client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=COGNITO_REGION,
)


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


@router.post(
    "/profile-image", 
    response_model=User,
    response_model_exclude={
        "cognito_user_data",
        "revision_id",
        "id",
    },
)
async def upload_image(
    file: UploadFile = File(description="A file read as UploadFile"),
    user: User = Depends(verify_token),
):
    allowed_extensions = AllowedExtensions(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
    allowed_file = allowed_extensions(file)

    try:
        filename = f"{user.sub_id}_photo.{allowed_file.filename.split('.')[-1]}"  # type: ignore

        if user.avatar_url:
            s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=filename)

        file_content = allowed_file.file.read()  # type: ignore

        resized_content = resize_image(file_content, (300, 300), allowed_file.filename.split(".")[-1])  # type: ignore
        s3_client.upload_fileobj(resized_content, AWS_BUCKET_NAME, filename)

        # Custom link generated p.s it does not expire
        url = f"https://{AWS_BUCKET_NAME}.s3-{COGNITO_REGION}.amazonaws.com/{filename}?v={datetime.utcnow().timestamp()}"

        await user.setValue({"avatar_url": url})

        return user
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=500, detail="AWS credentials not available")
