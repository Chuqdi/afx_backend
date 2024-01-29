import os
import json
from bson import ObjectId
from src.models.affirmation import Affirmation
from src.models.affirmation_listening_history import AffirmationListeningHistory
from src.models.affirmation_package import AffirmationPackage
from src.models.enums import TransactionSource
from src.models.user import User
from src.utils.affirmation import (
    calculate_time_difference_seconds,
    generate_random_sentences,
)
from src.utils.auth import verify_admin_token, verify_token
from src.utils.credit import remove_user_credit
from src.utils.logger import get_logger
from fastapi import APIRouter, Depends, Query
from fastapi import APIRouter, HTTPException, Path, status
from src.utils.response import paginate_response, success_response
from datetime import datetime

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

    # NOTE: Test mode only
    affirmation.audio_url = "https://res.cloudinary.com/daniel-goff/video/upload/v1706271596/viuweeztmbyhfybh3pop.mp3"

    affirmation.sentences = generate_random_sentences(4)

    createdAffirmation = await Affirmation.insert(affirmation)  # type: ignore

    if user.id:
        # Deduct the required credits from the user's account
        await remove_user_credit(
            user.id,
            int(credits_to_remove),
            source=TransactionSource.AFFIRMATION,
        )  # type: ignore

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
    starred: bool = Query(False, description="Filter by starred affirmations"),
    limit: int = Query(5, description="Number of top affirmations to retrieve"),
    package_id: str = Query(None, description="Enter package id"),
):
    query = {"user.sub_id": user.sub_id}

    # Add package_id to the query only if provided
    if package_id is not None:
        query["package._id"] = package_id

    # Add starred filter to the query
    if starred:
        query["starred"] = True  # type: ignore

    # Define the sorting key based on conditions
    sorting_key = (
        "-last_listened_at"
        if recently_listened
        else "-total_seconds_listened"
        if top_affirmation
        else "-created_at"
    )

    affirmations = (
        await Affirmation.find(
            query,
            fetch_links=True,
        )
        .sort(sorting_key)
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


@router.get("/listening-history/{affirmation_id}")
async def get_affirmation_listening_history(
    affirmation_id: str = Path(..., description="ID of the affirmation"),
    user: User = Depends(verify_token),
    page: int = Query(1, alias="page", description="Page number", ge=0),
    limit: int = Query(10, le=100, description="Items per page"),
):
    """Fetch all user's affrmation listening history with pagination"""
    resource_name = f"/listening-history/{affirmation_id}"
    start = (page - 1) * limit
    end = start + limit

    user_sub_id = user.sub_id if user else None
    search_filter = {
        "user.sub_id": user_sub_id,
        "affirmation._id": ObjectId(affirmation_id),
    }

    list = (
        await AffirmationListeningHistory.find(
            search_filter,
            fetch_links=True,
        )
        .sort("-created_at", "-updated_at")
        .to_list()
    )

    response = paginate_response(list, start, end, page, limit, resource_name)

    return success_response(
        response, "Affirmation listening history fetched successfully"
    )


@router.post("/listening-history/{affirmation_id}")
async def create(
    affirmation_listening_history: AffirmationListeningHistory,
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

    affirmation_listening_history.user = user_info  # type: ignore
    affirmation_listening_history.affirmation = affirmation  # type: ignore
    createdAffirmationHistory = await AffirmationListeningHistory.insert(affirmation_listening_history)  # type: ignore

    # NOTE Increment affirmation statistic
    seconds_to_increment = calculate_time_difference_seconds(
        affirmation_listening_history.start_at,
        affirmation_listening_history.listened_until,
    )

    affirmation.total_seconds_listened = affirmation.total_seconds_listened + seconds_to_increment  # type: ignore
    affirmation.last_listened_at = datetime.now()

    await affirmation.setValue(dict(affirmation))

    return success_response(
        createdAffirmationHistory,
        "Affirmation listening history created successfully",
        status.HTTP_201_CREATED,
    )


# Packages
@router.post("/packages")
async def create_afirmation_package(
    affirmationPackage: AffirmationPackage, _: User = Depends(verify_admin_token)
):
    created_package = await AffirmationPackage.insert(affirmationPackage)

    return success_response(
        created_package,
        "Affirmation package created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/packages")
async def get_affirmation_packages():
    data = await AffirmationPackage.find_all().to_list()

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
