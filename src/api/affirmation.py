import os
import json
from bson import ObjectId
from src.models.affirmation import Affirmation
from src.models.user import User
from src.utils.audio import blend_audio_from_urls
from src.utils.auth import verify_token
from src.utils.logger import get_logger
from fastapi import APIRouter, Depends
from fastapi import APIRouter, HTTPException, Path, status
from src.utils.response import success_response

router = APIRouter()
logger = get_logger("MAIN")


# Affirmations
@router.post("/")
async def create_affirmation(
    affirmation: Affirmation, user: User = Depends(verify_token)
):
    # TODO: Check user credit here and perform deductions
    # ...

    """Create New Affirmation Package"""
    affirmation.user = user  # type: ignore
    createdAffirmation = await Affirmation.insert(affirmation)  # type: ignore

    return success_response(
        createdAffirmation,
        "Affirmation created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/")
async def get_affirmations(user: User = Depends(verify_token)):
    affirmation = await Affirmation.find({"user.sub_id": user.sub_id}).to_list()
    return success_response(
        affirmation,
        "Affirmation fetched successfully",
        status.HTTP_200_OK,
    )


@router.put("/{id}")
async def update_affirmation_by_id(
    new_values: Affirmation,
    id: str = Path(..., description="ID of the affirmation"),
    user: User = Depends(verify_token),
):
    """Update Affirmation by ID"""
    affirmation = await Affirmation.find_one(
        {"user.sub_id": user.sub_id, "_id": ObjectId(id)},
    )
    if not affirmation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation not found",
        )
    await affirmation.setValue(dict(new_values))
    return success_response(message="Affirmation  updated successfully")


@router.delete("/{id}")
async def delete_affirmation_by_id(
    id: str = Path(..., description="ID of the Affirmation "),
    user: User = Depends(verify_token),
):
    """Delete Affirmation by ID"""
    affirmation = await Affirmation.find_one(
        {"user.sub_id": user.sub_id, "_id": ObjectId(id)},
    )
    if not affirmation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation  not found",
        )
    await affirmation.delete()  # type: ignore
    return success_response(message="Affirmation  deleted successfully")


# Packages
@router.get("/packages")
async def get_affirmation_packages():
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(
            current_directory, "..", "json", "affirmation-packages.json"
        )

        with open(json_file_path, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation package file not found",
        )

    return success_response(
        data,
        "Affirmation packages fetched successfully",
        status.HTTP_200_OK,
    )


# Background Sounds
@router.get("/background-sounds")
async def get_affirmation_background_sounds(_: User = Depends(verify_token)):
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(
            current_directory, "..", "json", "affirmation-background-sounds.json"
        )

        with open(json_file_path, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation background sound file not found",
        )

    return success_response(
        data,
        "Affirmation background sound fetched successfully",
        status.HTTP_200_OK,
    )


# Voices
@router.get("/voices")
async def get_affirmation_voices(_: User = Depends(verify_token)):
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(
            current_directory, "..", "json", "affirmation-voices.json"
        )

        with open(json_file_path, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation voices file not found",
        )

    return success_response(
        data,
        "Affirmation voices fetched successfully",
        status.HTTP_200_OK,
    )


# Categories
@router.get("/categories")
async def get_affirmation_categories():
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(
            current_directory, "..", "json", "affirmation-categories.json"
        )

        with open(json_file_path, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation categories file not found",
        )

    return success_response(
        data,
        "Affirmation categories fetched successfully",
        status.HTTP_200_OK,
    )


# Audio Blends
@router.post("/blend")
async def blend_audio(user: User = Depends(verify_token)):
    original_audio = "https://res.cloudinary.com/daniel-goff/video/upload/v1705684953/uploads/bzinylojzelggufzrpgg.mp3"
    background_audio = "https://cdn.pixabay.com/download/audio/2024/01/16/audio_e2b992254f.mp3?filename=better-day-186374.mp3"

    await blend_audio_from_urls(original_audio, background_audio)

    return success_response(
        data={},
        message="Blend successful",
        status_code=status.HTTP_200_OK,
    )
