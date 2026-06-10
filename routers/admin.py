# קובץ מנהלים
# אחראי על פעולות שמותרות רק למשתמש עם role של admin

from fastapi import APIRouter, Depends, HTTPException

from database import get_database_connection
from auth_service import get_current_user, require_admin


router = APIRouter(
    prefix = "/admin",
    tags = ["admin"]
)


# שליפת כל המשתמשים במערכת
@router.get("/users")
def get_all_users(current_user=Depends(get_current_user)):
    require_admin(current_user)

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, email, role
        FROM users
        ORDER BY id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "role": row[3]
        })

    return {
        "users": users
    }


# מחיקת משתמש לפי id
@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user=Depends(get_current_user)):
    require_admin(current_user)

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = %s;
    """, (user_id,))

    deleted_count = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    if deleted_count == 0:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )

    return {
        "message": "User deleted successfully"
    }


# מחיקת תגובה לפי id
@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user=Depends(get_current_user)):
    require_admin(current_user)

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM comments
        WHERE id = %s;
    """, (comment_id,))

    deleted_count = cursor.rowcount

    connection.commit()

    cursor.close()
    connection.close()

    if deleted_count == 0:
        raise HTTPException(
            status_code = 404,
            detail = "Comment not found"
        )

    return {
        "message": "Comment deleted successfully"
    }