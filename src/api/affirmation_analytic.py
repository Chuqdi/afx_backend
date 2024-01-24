from src.models.affirmation import Affirmation
from src.models.user import User
from src.utils.auth import verify_token
from src.utils.logger import get_logger
from fastapi import APIRouter, Depends, status
from src.utils.response import success_response
from datetime import datetime


router = APIRouter()
logger = get_logger("MAIN")


@router.get("/streak-information")
async def get_user_streak_info(user: User = Depends(verify_token)):
    """Getting User affirmation streak information"""

    affirmations = await Affirmation.find(
        {"user.sub_id": user.sub_id}, fetch_links=True
    ).to_list()

    streak_info = {}
    current_streak = 0
    total_affirmations = 0
    total_seconds_listened = 0
    total_affirmations_this_week = 0
    total_seconds_listened_this_week = 0
    today = datetime.now().date()

    for affirmation in affirmations:
        total_affirmations += 1
        total_seconds_listened += affirmation.total_seconds_listened


        if affirmation.completed_at:
            completed_date = affirmation.completed_at.date()

            # Check if the completed date is consecutive
            if (today - completed_date).days == 1:
                current_streak += 1
            else:
                current_streak = 1

            # Check if the affirmation was completed this week
            if completed_date.strftime('%U') == today.strftime('%U'):
                total_affirmations_this_week += 1
                total_seconds_listened_this_week += affirmation.total_seconds_listened


            streak_info.setdefault(str(completed_date.year), {})
            streak_info[str(completed_date.year)].setdefault(
                f"{completed_date.strftime('%U')}", {}
            )
            streak_info[str(completed_date.year)][
                f"{completed_date.strftime('%U')}"
            ][completed_date.strftime("%a").lower()] = True

    # Set other days to False if they have not been completed
    for year in streak_info:
        for week in streak_info[year]:
            for day in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                streak_info[year][week].setdefault(day, False)

    streak_info["current_streak"] = current_streak
    streak_info['total_affirmations'] = total_affirmations
    streak_info['total_seconds_listened'] = total_seconds_listened
    streak_info['total_affirmations_this_week'] = total_affirmations_this_week
    streak_info['total_seconds_listened_this_week'] = total_seconds_listened_this_week

    
    return success_response(
        streak_info,
        "User affirmation streak information fetched successfully",
        status.HTTP_200_OK,
    )
