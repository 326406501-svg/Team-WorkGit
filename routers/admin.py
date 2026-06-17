# Admin router
# Handles the admin dashboard:
# 1. Admin login
# 2. View users with search and pagination
# 3. Delete users
# 4. View comments with pagination
# 5. Delete comments
# 6. Send news update emails

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_database_connection
from news_service import fetch_news_by_category
from message import send_news_update_email


router = APIRouter()

templates = Jinja2Templates(directory = "html")

ITEMS_PER_PAGE = 10


# Check if the current user is an admin.
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


# Returns users with pagination and optional search by username or email.
def get_users_from_db(search = "", limit = ITEMS_PER_PAGE, offset = 0):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, email, role
        FROM users
        WHERE username ILIKE %s
        OR email ILIKE %s
        ORDER BY id
        LIMIT %s OFFSET %s;
    """, (f"%{search}%", f"%{search}%", limit, offset))

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


# Counts users after applying the search filter.
# This helps us know if the Next button should be displayed.
def count_users_from_db(search = ""):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE username ILIKE %s
        OR email ILIKE %s;
    """, (f"%{search}%", f"%{search}%"))

    total_users = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_users


# Returns comments with pagination and optional search.
def get_comments_from_db(
    search="",
    limit=ITEMS_PER_PAGE,
    offset=0
):
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
        WHERE users.username ILIKE %s
        OR comments.comment_text ILIKE %s
        ORDER BY comments.created_at DESC
        LIMIT %s OFFSET %s;
    """, (
        f"%{search}%",
        f"%{search}%",
        limit,
        offset
    ))

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



# Counts comments after applying search.
def count_comments_from_db(search=""):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE users.username ILIKE %s
        OR comments.comment_text ILIKE %s;
    """, (
        f"%{search}%",
        f"%{search}%"
    ))

    total_comments = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_comments

# Builds all dashboard data in one place.
# This keeps the routes cleaner and easier to read.
def get_admin_dashboard_context(
    admin_username,
    admin_password,
    search = "",
    comments_search = "",
    users_offset = 0,
    comments_offset = 0,
    message = None
):
    users = get_users_from_db(
        search = search,
        limit = ITEMS_PER_PAGE,
        offset = users_offset
    )

    comments = get_comments_from_db(
        search = comments_search,
        limit = ITEMS_PER_PAGE,
        offset = comments_offset
    )

    total_users = count_users_from_db(search)
    total_comments = count_comments_from_db(
        comments_search
    )

    users_previous_offset = users_offset - ITEMS_PER_PAGE
    users_next_offset = users_offset + ITEMS_PER_PAGE

    comments_previous_offset = comments_offset - ITEMS_PER_PAGE
    comments_next_offset = comments_offset + ITEMS_PER_PAGE

    return {
        "admin_username": admin_username,
        "admin_password": admin_password,

        "users": users,
        "comments": comments,

        "search": search,
        "comments_search": comments_search,

        "users_offset": users_offset,
        "comments_offset": comments_offset,
        "limit": ITEMS_PER_PAGE,

        "users_previous_offset": users_previous_offset,
        "users_next_offset": users_next_offset,
        "comments_previous_offset": comments_previous_offset,
        "comments_next_offset": comments_next_offset,

        "has_previous_users": users_offset > 0,
        "has_next_users": users_next_offset < total_users,

        "has_previous_comments": comments_offset > 0,
        "has_next_comments": comments_next_offset < total_comments,

        "total_users": total_users,
        "total_comments": total_comments,

        "message": message
    }


# Shows the admin login page.
@router.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "admin_login.html"
    )


# Opens the admin dashboard after login.
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

    context = get_admin_dashboard_context(
        admin_username = username,
        admin_password = password
    )

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = context
    )


# Reloads the dashboard with search and pagination values.
@router.post("/admin/dashboard/filter", response_class=HTMLResponse)
def filter_admin_dashboard(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    search: str = Form(""),
    comments_search: str = Form(""),
    users_offset: int = Form(0),
    comments_offset: int = Form(0)
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

    if users_offset < 0:
        users_offset = 0

    if comments_offset < 0:
        comments_offset = 0

    context = get_admin_dashboard_context(
        admin_username = admin_username,
        admin_password = admin_password,
        search = search,
        comments_search = comments_search,
        users_offset = users_offset,
        comments_offset = comments_offset
    )

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = context
    )


# Deletes a regular user from the system.
@router.post("/admin/delete_user", response_class=HTMLResponse)
def delete_user_from_admin(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    user_id: int = Form(...),
    search: str = Form(""),
    users_offset: int = Form(0),
    comments_offset: int = Form(0)
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

        context = get_admin_dashboard_context(
            admin_username = admin_username,
            admin_password = admin_password,
            search = search,
            users_offset = users_offset,
            comments_offset = comments_offset,
            message = "User not found."
        )

        return templates.TemplateResponse(
            request = request,
            name = "admin_dashboard.html",
            context = context
        )

    if user_id == admin_user[0]:
        cursor.close()
        connection.close()

        context = get_admin_dashboard_context(
            admin_username = admin_username,
            admin_password = admin_password,
            search = search,
            users_offset = users_offset,
            comments_offset = comments_offset,
            message = "You cannot delete your own admin account."
        )

        return templates.TemplateResponse(
            request = request,
            name = "admin_dashboard.html",
            context = context
        )

    if user_to_delete[0] == "admin":
        cursor.close()
        connection.close()

        context = get_admin_dashboard_context(
            admin_username = admin_username,
            admin_password = admin_password,
            search = search,
            users_offset = users_offset,
            comments_offset = comments_offset,
            message = "Admin users cannot be deleted."
        )

        return templates.TemplateResponse(
            request = request,
            name = "admin_dashboard.html",
            context = context
        )

    cursor.execute("""
        DELETE FROM users
        WHERE id = %s;
    """, (user_id,))

    connection.commit()

    cursor.close()
    connection.close()

    context = get_admin_dashboard_context(
        admin_username = admin_username,
        admin_password = admin_password,
        search = search,
        users_offset = users_offset,
        comments_offset = comments_offset,
        message = "User deleted successfully."
    )

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = context
    )


# Deletes a comment from the system.
@router.post("/admin/delete_comment", response_class=HTMLResponse)
def delete_comment_from_admin(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    comment_id: int = Form(...),
    search: str = Form(""),
    users_offset: int = Form(0),
    comments_offset: int = Form(0)
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

    context = get_admin_dashboard_context(
        admin_username = admin_username,
        admin_password = admin_password,
        search = search,
        users_offset = users_offset,
        comments_offset = comments_offset,
        message = "Comment deleted successfully."
    )

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = context
    )


# Sends a news update email preview to all users.
@router.post("/admin/send_news_update", response_class=HTMLResponse)
def send_news_update_from_admin(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...),
    search: str = Form(""),
    users_offset: int = Form(0),
    comments_offset: int = Form(0)
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

    users = get_users_from_db(
        search = "",
        limit = 100000,
        offset = 0
    )

    articles = fetch_news_by_category("world", 3)

    for user in users:
        send_news_update_email(
            user["username"],
            user["email"],
            articles
        )

    context = get_admin_dashboard_context(
        admin_username = admin_username,
        admin_password = admin_password,
        search = search,
        users_offset = users_offset,
        comments_offset = comments_offset,
        message = "News update email preview was sent to all users."
    )

    return templates.TemplateResponse(
        request = request,
        name = "admin_dashboard.html",
        context = context
    )