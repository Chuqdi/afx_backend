from bson import ObjectId
from src.models.affirmation_background_sound import AffirmationBackgroundSound
from src.models.affirmation_package import AffirmationPackage, AffirmationPackageInput
from src.models.affirmation_voice import AffirmationVoice
from src.models.field import Field
from src.utils.logger import get_logger
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Path, status
from src.utils.response import success_response

router = APIRouter()
logger = get_logger("MAIN")


# Packages
@router.post("/packages")
async def create_affirmation_package(
    package: AffirmationPackageInput,
):
    """Create New Affirmation Package"""

    # Checks
    background_sounds = [
        await AffirmationBackgroundSound.get(ObjectId(sound_id))
        for sound_id in package.affirmation_background_sounds
    ]

    if None in background_sounds:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oops, you have supplied invalid affirmation_background_sound id",
        )

    voices = [
        await AffirmationVoice.get(ObjectId(voice_id))
        for voice_id in package.affirmation_voices
    ]

    if None in voices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oops, you have supplied invalid affirmation_voice id",
        )

    package.affirmation_voices = voices  # type: ignore
    package.affirmation_background_sounds = background_sounds  # type: ignore

    createdAffirmationVoice = await AffirmationPackage.insert(package)  # type: ignore

    return success_response(
        createdAffirmationVoice,
        "Affirmation package created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/packages")
async def get_affirmation_packages():
    all_background_sounds = await AffirmationPackage.find_all().to_list()
    return success_response(
        all_background_sounds,
        "Affirmation packages fetched successfully",
        status.HTTP_200_OK,
    )


@router.put("/packages/{id}")
async def update_affirmation_package_by_id(
    new_values: AffirmationPackage,
    id: str = Path(..., description="ID of the affirmation package"),
):
    """Update Affirmation package by ID"""
    existing_background_sound = await AffirmationPackage.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation package not found",
        )
    await existing_background_sound.setValue(dict(new_values))
    return success_response(message="Affirmation package updated successfully")


@router.delete("/packages/{id}")
async def delete_affirmation_package_by_id(
    id: str = Path(..., description="ID of the Affirmation package"),
):
    """Delete Affirmation package by ID"""
    existing_background_sound = await AffirmationPackage.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affirmation package not found",
        )
    await existing_background_sound.delete()  # type: ignore
    return success_response(message="Affirmation package deleted successfully")


# Voices
@router.post("/voices")
async def create_affirmation_voice(
    voice: AffirmationVoice,
):
    """Create New Background Sound"""
    createdAffirmationVoice = await AffirmationVoice.insert(voice)  # type: ignore
    return success_response(
        createdAffirmationVoice,
        "Affirmation voice created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/voices")
async def get_affirmation_voices():
    all_background_sounds = await AffirmationVoice.find_all().to_list()
    return success_response(
        all_background_sounds,
        "Affirmation voices fetched successfully",
        status.HTTP_200_OK,
    )


@router.put("/voices/{id}")
async def update_affirmation_voice_by_id(
    new_values: AffirmationVoice,
    id: str = Path(..., description="ID of the affirmation voice"),
):
    """Update Affirmation voice by ID"""
    existing_background_sound = await AffirmationVoice.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Affirmation voice not found"
        )
    await existing_background_sound.setValue(dict(new_values))
    return success_response(message="Affirmation voice updated successfully")


@router.delete("/voices/{id}")
async def delete_affirmation_voice_by_id(
    id: str = Path(..., description="ID of the Affirmation voice"),
):
    """Delete Affirmation voice by ID"""
    existing_background_sound = await AffirmationVoice.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Affirmation voice not found"
        )
    await existing_background_sound.delete()  # type: ignore
    return success_response(message="Affirmation voice deleted successfully")


# Background sounds
@router.post("/background-sounds")
async def create_affirmation_background_sound(
    backgroundSound: AffirmationBackgroundSound,
):
    """Create New Background Sound"""
    createdBackgroundSound = await AffirmationBackgroundSound.insert(backgroundSound)  # type: ignore
    return success_response(
        createdBackgroundSound,
        "Background sound created successfully",
        status.HTTP_201_CREATED,
    )


@router.get("/background-sounds")
async def get_affirmation_background_sounds():
    all_background_sounds = await AffirmationBackgroundSound.find_all().to_list()
    return success_response(
        all_background_sounds,
        "Background sounds fetched successfully",
        status.HTTP_200_OK,
    )


@router.put("/background-sounds/{id}")
async def update_affirmation_background_sound_by_id(
    new_values: AffirmationBackgroundSound,
    id: str = Path(..., description="ID of the affirmation background sound"),
):
    """Update Background Sound by ID"""
    existing_background_sound = await AffirmationBackgroundSound.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Background sound not found"
        )
    await existing_background_sound.setValue(dict(new_values))
    return success_response(message="Background sound updated successfully")


@router.delete("/background-sounds/{id}")
async def delete_affirmation_background_sound_by_id(
    id: str = Path(..., description="ID of the background sound"),
):
    """Delete background sound by ID"""
    existing_background_sound = await AffirmationBackgroundSound.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_background_sound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Background sound not found"
        )
    await existing_background_sound.delete()  # type: ignore
    return success_response(message="Background sound deleted successfully")


# Fields
@router.post("/fields")
async def create_field(field: Field):
    """Create a new Field"""
    # Prevent creation of duplicate fields
    existing_field = await Field.find_one(Field.key == field.key)

    if existing_field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Field already exists"
        )

    createdField = await Field.insert(field)  # type: ignore
    return success_response(
        createdField, "Field created successfully", status.HTTP_201_CREATED
    )


@router.get("/fields")
async def get_fields():
    all_fields = await Field.find_all().to_list()
    return success_response(
        all_fields, "Fields fetched successfully", status.HTTP_200_OK
    )


@router.get("/fields/{id}")
async def get_field_by_id(
    id: str = Path(..., description="ID of the field"),
):
    """Fetch a single field by ID"""
    field = await Field.find_one({"_id": ObjectId(id)})
    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Field not found"
        )
    return success_response(field, "Field fetched successfully")


@router.put("/fields/{id}")
async def update_field_by_id(
    new_values: Field,
    id: str = Path(..., description="ID of the field"),
):
    """Update a field by ID"""
    existing_field = await Field.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Field not found"
        )
    await existing_field.setValue(dict(new_values))
    return success_response(message="Field updated successfully")


@router.delete("/fields/{id}")
async def delete_field_by_id(
    id: str = Path(..., description="ID of the field"),
):
    """Delete a field by ID"""
    existing_field = await Field.find_one(
        {"_id": ObjectId(id)},
    )
    if not existing_field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Field not found"
        )
    await existing_field.delete()  # type: ignore
    return success_response(message="Field deleted successfully")
