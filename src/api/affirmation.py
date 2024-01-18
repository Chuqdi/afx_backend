import os
import json
from bson import ObjectId
from src.models.affirmation import Affirmation
from src.utils.logger import get_logger
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Path, status
from src.utils.response import success_response

router = APIRouter()
logger = get_logger("MAIN")


# Affirmations
@router.post("/")
async def create_affirmation(
    affirmation: Affirmation,
):
    # TODO: Check user credit here
    # ...

    """Create New Affirmation Package"""
    createdAffirmation = await Affirmation.insert(affirmation)  # type: ignore

    return success_response(
        createdAffirmation,
        "Affirmation created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/")
async def get_affirmations():
    all_background_sounds = await Affirmation.find_all().to_list()
    return success_response(
        all_background_sounds,
        "Affirmation fetched successfully",
        status.HTTP_200_OK,
    )


@router.put("/{id}")
async def update_affirmation_by_id(
    new_values: Affirmation,
    id: str = Path(..., description="ID of the affirmation"),
):
    """Update Affirmation by ID"""
    existing_background_sound = await Affirmation.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation not found",
        )
    await existing_background_sound.setValue(dict(new_values))
    return success_response(message="Affirmation  updated successfully")


@router.delete("/{id}")
async def delete_affirmation_by_id(
    id: str = Path(..., description="ID of the Affirmation "),
):
    """Delete Affirmation by ID"""
    existing_background_sound = await Affirmation.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation  not found",
        )
    await existing_background_sound.delete()  # type: ignore
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
async def get_affirmation_background_sounds():
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
async def get_affirmation_voices():
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
