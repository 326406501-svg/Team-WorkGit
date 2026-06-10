# קובץ תחומי עניין
# אחראי על שמירה ושליפה של תחומי עניין למשתמש רשום

from fastapi import APIRouter, Depends

from database import get_database_connection
from models import Interest
from auth_service import get_current_user


router = APIRouter(
    prefix = "/interests",
    tags = ["interests"]
)


# הוספת תחום עניין למשתמש המחובר
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


# שליפת תחומי העניין של המשתמש המחובר
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