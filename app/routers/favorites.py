# Ã—Â§Ã—â€¢Ã—â€˜Ã—Â¥ Ã—Å¾Ã—â€¢Ã—Â¢Ã—â€œÃ—Â¤Ã—â„¢Ã—Â
# Ã—ÂÃ—â€”Ã—Â¨Ã—ÂÃ—â„¢ Ã—Â¢Ã—Å“ Ã—Â©Ã—Å¾Ã—â„¢Ã—Â¨Ã—Âª Ã—â€ºÃ—ÂªÃ—â€˜Ã—â€¢Ã—Âª Ã—Å¾Ã—â€¢Ã—Â¢Ã—â€œÃ—Â¤Ã—â€¢Ã—Âª Ã—â€¢Ã—Â©Ã—Å“Ã—â„¢Ã—Â¤Ã—ÂªÃ—Å¸ Ã—Å“Ã—Å¾Ã—Â©Ã—ÂªÃ—Å¾Ã—Â© Ã—Â¨Ã—Â©Ã—â€¢Ã—Â

from fastapi import APIRouter, Depends

from app.database import get_database_connection
from app.models import FavoriteArticle
from app.services.auth_service import get_current_user


router = APIRouter(
    prefix = "/favorites",
    tags = ["favorites"]
)


# Ã—Â©Ã—Å¾Ã—â„¢Ã—Â¨Ã—Âª Ã—â€ºÃ—ÂªÃ—â€˜Ã—â€ Ã—â€˜Ã—Å¾Ã—â€¢Ã—Â¢Ã—â€œÃ—Â¤Ã—â„¢Ã—Â
@router.post("/")
def add_favorite(
    article: FavoriteArticle,
    current_user = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO favorites (
            user_id,
            article_id,
            title,
            url,
            image,
            source,
            category
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        user_id,
        article.url,      # Ã—Å¾Ã—Â©Ã—Å¾Ã—Â© Ã—â€º-id Ã—â„¢Ã—â„¢Ã—â€”Ã—â€¢Ã—â€œÃ—â„¢ Ã—â€ºÃ—Â¨Ã—â€™Ã—Â¢
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


# Ã—Â©Ã—Å“Ã—â„¢Ã—Â¤Ã—Âª Ã—â€ºÃ—Å“ Ã—â€Ã—Å¾Ã—â€¢Ã—Â¢Ã—â€œÃ—Â¤Ã—â„¢Ã—Â Ã—Â©Ã—Å“ Ã—â€Ã—Å¾Ã—Â©Ã—ÂªÃ—Å¾Ã—Â©
@router.get("/me")
def get_my_favorites(
    current_user = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            article_id,
            title,
            url,
            image,
            source,
            category
        FROM favorites
        WHERE user_id = %s
        ORDER BY id DESC;
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    favorites = []

    for row in rows:
        favorites.append({
            "id": row[0],
            "article_id": row[1],
            "title": row[2],
            "url": row[3],
            "image": row[4],
            "source": row[5],
            "category": row[6]
        })

    return {
        "favorites": favorites
    }


# Ã—Å¾Ã—â€”Ã—â„¢Ã—Â§Ã—Âª Ã—â€ºÃ—ÂªÃ—â€˜Ã—â€ Ã—Å¾Ã—â€Ã—Å¾Ã—â€¢Ã—Â¢Ã—â€œÃ—Â¤Ã—â„¢Ã—Â
@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    current_user = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM favorites
        WHERE id = %s
        AND user_id = %s;
    """, (
        favorite_id,
        user_id
    ))

    deleted_count = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    if deleted_count == 0:
        return {
            "message": "Favorite not found"
        }

    return {
        "message": "Favorite deleted successfully"
    }