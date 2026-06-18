# Ã—Â§Ã—â€¢Ã—â€˜Ã—Â¥ Ã—ÂªÃ—â€”Ã—â€¢Ã—Å¾Ã—â„¢ Ã—Â¢Ã—Â Ã—â„¢Ã—â„¢Ã—Å¸
# Ã—ÂÃ—â€”Ã—Â¨Ã—ÂÃ—â„¢ Ã—Â¢Ã—Å“ Ã—Â©Ã—Å¾Ã—â„¢Ã—Â¨Ã—â€ Ã—â€¢Ã—Â©Ã—Å“Ã—â„¢Ã—Â¤Ã—â€ Ã—Â©Ã—Å“ Ã—ÂªÃ—â€”Ã—â€¢Ã—Å¾Ã—â„¢ Ã—Â¢Ã—Â Ã—â„¢Ã—â„¢Ã—Å¸ Ã—Å“Ã—Å¾Ã—Â©Ã—ÂªÃ—Å¾Ã—Â© Ã—Â¨Ã—Â©Ã—â€¢Ã—Â

from fastapi import APIRouter, Depends

from app.database import get_database_connection
from app.models import Interest
from app.services.auth_service import get_current_user


router = APIRouter(
    prefix = "/interests",
    tags = ["interests"]
)


# Ã—â€Ã—â€¢Ã—Â¡Ã—Â¤Ã—Âª Ã—ÂªÃ—â€”Ã—â€¢Ã—Â Ã—Â¢Ã—Â Ã—â„¢Ã—â„¢Ã—Å¸ Ã—Å“Ã—Å¾Ã—Â©Ã—ÂªÃ—Å¾Ã—Â© Ã—â€Ã—Å¾Ã—â€”Ã—â€¢Ã—â€˜Ã—Â¨
@router.post("/")
def add_interest(interest: Interest, current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO interests (user_id, category)
        VALUES (%s, %s);
    """, (user_id, interest.category))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Interest saved successfully",
        "user_id": user_id,
        "category": interest.category
    }


# Ã—Â©Ã—Å“Ã—â„¢Ã—Â¤Ã—Âª Ã—ÂªÃ—â€”Ã—â€¢Ã—Å¾Ã—â„¢ Ã—â€Ã—Â¢Ã—Â Ã—â„¢Ã—â„¢Ã—Å¸ Ã—Â©Ã—Å“ Ã—â€Ã—Å¾Ã—Â©Ã—ÂªÃ—Å¾Ã—Â© Ã—â€Ã—Å¾Ã—â€”Ã—â€¢Ã—â€˜Ã—Â¨
@router.get("/me")
def get_my_interests(current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category
        FROM interests
        WHERE user_id = %s;
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    interests = [row[0] for row in rows]

    return {
        "user_id": user_id,
        "interests": interests
    }