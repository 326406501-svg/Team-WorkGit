# קובץ מועדפים
# אחראי על שמירת כתבות מועדפות ושליפתן למשתמש רשום

from fastapi import APIRouter, Depends

from database import get_database_connection
from models import FavoriteArticle
from auth_service import get_current_user


router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)


# שמירת כתבה במועדפים
@router.post("/")
def add_favorite(article: FavoriteArticle, current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO favorites (user_id, title, url, image, source, category)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        user_id,
        article.title,
        article.url,
        article.image,
        article.source,
        article.category
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Article added to favorites"
    }


# שליפת המועדפים של המשתמש
@router.get("/me")
def get_my_favorites(current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, url, image, source, category
        FROM favorites
        WHERE user_id = %s;
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    favorites = []

    for row in rows:
        favorites.append({
            "id": row[0],
            "title": row[1],
            "url": row[2],
            "image": row[3],
            "source": row[4],
            "category": row[5]
        })

    return {
        "favorites": favorites
    }