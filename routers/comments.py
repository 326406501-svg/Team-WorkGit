# קובץ תגובות
# אחראי על הוספת תגובות ושליפת תגובות לפי כתבה

from fastapi import APIRouter, Depends

from database import get_database_connection
from models import CommentCreate
from auth_service import get_current_user


router = APIRouter(
    prefix = "/comments",
    tags = ["comments"]
)


# הוספת תגובה לכתבה
@router.post("/")
def add_comment(comment: CommentCreate, current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO comments (user_id, article_url, comment_text)
        VALUES (%s, %s, %s);
    """, (
        user_id,
        comment.article_url,
        comment.comment_text
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Comment added successfully"
    }


# שליפת תגובות לפי כתבה
@router.get("/")
def get_comments_by_article(article_url: str):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT comments.id, users.username, comments.comment_text, comments.created_at
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.article_url = %s
        ORDER BY comments.created_at DESC;
    """, (article_url,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    comments = []

    for row in rows:
        comments.append({
            "comment_id": row[0],
            "username": row[1],
            "comment": row[2],
            "created_at": row[3]
        })

    return {
        "comments": comments
    }