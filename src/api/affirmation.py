import os
import json
from bson import ObjectId
from src.models.affirmation import Affirmation
from src.models.affirmation_listening_history import AffirmationListeningHistory
from src.models.enums import TransactionSource
from src.models.user import User
from src.utils.auth import verify_token
from src.utils.credit import remove_user_credit
from src.utils.logger import get_logger
from fastapi import APIRouter, Depends, Query
from fastapi import APIRouter, HTTPException, Path, status
from src.utils.response import success_response

router = APIRouter()
logger = get_logger("MAIN")


# Affirmations
@router.post("/")
async def create_affirmation(
    affirmation: Affirmation, user: User = Depends(verify_token)
):
    credits_to_remove = affirmation.package.get("credits", 1)  # type: ignore
    # Check credit
    if user.credits < credits_to_remove:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient credits"
        )

    """Create New Affirmation Package"""
    affirmation.user = user  # type: ignore
    createdAffirmation = await Affirmation.insert(affirmation)  # type: ignore

    if user.id:
        # Deduct the required credits from the user's account
        await remove_user_credit(
            user.id,
            int(credits_to_remove),
            source=TransactionSource.AFFIRMATION,
        ) # type: ignore

    return success_response(
        createdAffirmation,
        "Affirmation created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/")
async def get_affirmations(
    user: User = Depends(verify_token),
    recently_listened: bool = Query(
        False, description="Filter by recently listened affirmations"
    ),
    top_affirmation: bool = Query(False, description="Filter by top X affirmations"),
    limit: int = Query(5, description="Number of top affirmations to retrieve"),
    package_id: int = Query(0, description="Enter package id"),
):
    query = (
        {"user.sub_id": user.sub_id, "package.id": package_id}
        if package_id
        else {"user.sub_id": user.sub_id}
    )
    affirmations = (
        await Affirmation.find(
            query,
            fetch_links=True,
        )
        .sort(
            "-last_listened_at"
            if recently_listened
            else "-total_seconds_listened"
            if top_affirmation
            else "-created_at"
        )
        .limit(limit)
        .to_list()
    )

    return success_response(
        affirmations,
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


@router.post("/listening-history/{affirmation_id}")
async def create(
    affirmationListeningHistory: AffirmationListeningHistory,
    affirmation_id: str = Path(..., description="ID of the Affirmation "),
    user_info: User = Depends(verify_token),
):
    """Create a new affirmation history"""
    affirmation = await Affirmation.find_one(
        {"user.sub_id": user_info.sub_id, "_id": ObjectId(affirmation_id)},
        fetch_links=True,
    )

    if not affirmation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation  not found",
        )


    affirmationListeningHistory.user = user_info  # type: ignore
    affirmationListeningHistory.affirmation = affirmation  # type: ignore
    createdAffirmationHistory = await AffirmationListeningHistory.insert(affirmationListeningHistory)  # type: ignore
    return success_response(
        createdAffirmationHistory,
        "Affirmation listening history created successfully",
        status.HTTP_201_CREATED,
    )


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
