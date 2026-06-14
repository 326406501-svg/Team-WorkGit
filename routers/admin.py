# קובץ מנהלים
# אחראי על דף ניהול בסיסי:
# 1. צפייה בכל המשתמשים
# 2. מחיקת משתמש
# 3. צפייה בכל התגובות
# 4. מחיקת תגובה
# 5. שליחת עדכון חדשות למיילים - כרגע כ-preview בטרמינל

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_database_connection
from news_service import fetch_news_by_category
from message import send_news_update_email


router = APIRouter()

templates = Jinja2Templates(directory = "html")


def check_admin(username, password):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, role
        FROM users
        WHERE username = %s
        AND password = %s
        AND role = 'admin';
    """, (username, password))

    admin_user = cursor.fetchone()

    cursor.close()
    connection.close()

    return admin_user


def get_all_users_from_db():
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

    return users


def get_all_comments_from_db():
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            comments.id,
            users.username,
            comments.article_url,
            comments.comment_text,
            comments.created_at
        FROM comments
        JOIN users ON comments.user_id = users.id
        ORDER BY comments.created_at DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    comments = []

    for row in rows:
        comments.append({
            "id": row[0],
            "username": row[1],
            "article_url": row[2],
            "comment_text": row[3],
            "created_at": row[4]
        })

    return comments


@router.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "admin_login.html"
    )


@router.post("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    admin_user = check_admin(username, password)

    if admin_user is None:
        return templates.TemplateResponse(
            request = request,
            name = "status.html",
            context = {
                "status_code": "Access denied. Admin only."
            }
        )

    users = get_all_users_from_db()
    comments = get_all_comments_from_db()

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = {
            "admin_username": username,
            "admin_password": password,
            "users": users,
            "comments": comments
        }
    )


@router.post("/admin/delete_user", response_class=HTMLResponse)
def delete_user_from_admin(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    user_id: int = Form(...)
):
    admin_user = check_admin(admin_username, admin_password)

    if admin_user is None:
        return templates.TemplateResponse(
            request = request,
            name = "status.html",
            context = {
                "status_code": "Access denied. Admin only."
            }
        )

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role
        FROM users
        WHERE id = %s;
    """, (user_id,))

    user_to_delete = cursor.fetchone()

    if user_to_delete is None:
        cursor.close()
        connection.close()

        return templates.TemplateResponse(
            request = request,
            name = "admin_dashboard.html",
            context = {
                "admin_username": admin_username,
                "admin_password": admin_password,
                "users": get_all_users_from_db(),
                "comments": get_all_comments_from_db(),
                "message": "User not found."
            }
        )

    if user_id == admin_user[0]:
        cursor.close()
        connection.close()

        return templates.TemplateResponse(
            request = request,
            name = "admin_dashboard.html",
            context = {
                "admin_username": admin_username,
                "admin_password": admin_password,
                "users": get_all_users_from_db(),
                "comments": get_all_comments_from_db(),
                "message": "You cannot delete your own admin account."
            }
        )

    if user_to_delete[0] == "admin":
        cursor.close()
        connection.close()

        return templates.TemplateResponse(
            request = request,
            name = "admin_dashboard.html",
            context = {
                "admin_username": admin_username,
                "admin_password": admin_password,
                "users": get_all_users_from_db(),
                "comments": get_all_comments_from_db(),
                "message": "Admin users cannot be deleted."
            }
        )

    cursor.execute("""
        DELETE FROM users
        WHERE id = %s;
    """, (user_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = {
            "admin_username": admin_username,
            "admin_password": admin_password,
            "users": get_all_users_from_db(),
            "comments": get_all_comments_from_db(),
            "message": "User deleted successfully."
        }
    )


@router.post("/admin/delete_comment", response_class=HTMLResponse)
def delete_comment_from_admin(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    comment_id: int = Form(...)
):
    admin_user = check_admin(admin_username, admin_password)

    if admin_user is None:
        return templates.TemplateResponse(
            request = request,
            name = "status.html",
            context = {
                "status_code": "Access denied. Admin only."
            }
        )

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM comments
        WHERE id = %s;
    """, (comment_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = {
            "admin_username": admin_username,
            "admin_password": admin_password,
            "users": get_all_users_from_db(),
            "comments": get_all_comments_from_db(),
            "message": "Comment deleted successfully."
        }
    )


@router.post("/admin/send_news_update", response_class=HTMLResponse)
def send_news_update_from_admin(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...)
):
    admin_user = check_admin(admin_username, admin_password)

    if admin_user is None:
        return templates.TemplateResponse(
            request = request,
            name = "status.html",
            context = {
                "status_code": "Access denied. Admin only."
            }
        )

    users = get_all_users_from_db()
    articles = fetch_news_by_category("world", 3)

    for user in users:
        send_news_update_email(
            user["username"],
            user["email"],
            articles
        )

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = {
            "admin_username": admin_username,
            "admin_password": admin_password,
            "users": users,
            "comments": get_all_comments_from_db(),
            "message": "News update email preview was sent to all users in the terminal."
        }
    )