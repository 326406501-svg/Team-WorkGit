# ×§×•×‘×¥ ×ž×©×ª×ž×©×™×
# ××—×¨××™ ×¢×œ ×”×¨×©×ž×ª ×ž×©×ª×ž×©×™× ×—×“×©×™× ×ž×ª×•×š register.html
# ×‘×ž×§×•× ×œ×©×ž×•×¨ ×‘-users.json, ×× ×—× ×• ×©×•×ž×¨×™× ×‘×˜×‘×œ×ª users ×‘-PostgreSQL

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.paths import TEMPLATES_DIR
from app.database import get_database_connection
from app.routers.intersects import get_status
from app.services.message import send_welcome_email


router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ×”×¨×©×ž×ª ×ž×©×ª×ž×© ×—×“×©
# ×ž×§×‘×œ username, password, email ×ž×”×˜×•×¤×¡ ×©×œ register.html
@router.post("/register", response_class = HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    connection = get_database_connection()
    cursor = connection.cursor()

    # ×‘×“×™×§×” ×× username ××• email ×›×‘×¨ ×§×™×™×ž×™× ×‘×ž×¡×“ ×”× ×ª×•× ×™×
    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = %s OR email = %s;
    """, (username, email))

    existing_user = cursor.fetchone()

    if existing_user is not None:
        cursor.close()
        connection.close()

        return get_status(
            "Username or email already exists! Please choose another one.",
            request
        )

    # ×‘×“×™×§×ª ××•×¨×š ×¡×™×¡×ž×”
    if len(password) < 6 or len(password) > 10:
        cursor.close()
        connection.close()

        return get_status(
            "Invalid password! Must be between 6 and 10 characters.",
            request
        )

    # ×”×›× ×¡×ª ×”×ž×©×ª×ž×© ×”×—×“×© ×œ×˜×‘×œ×ª users
    cursor.execute("""
        INSERT INTO users (username, password, email, role)
        VALUES (%s, %s, %s, %s);
    """, (username, password, email, "user"))

    connection.commit()

    cursor.close()
    connection.close()

    send_welcome_email(
        username,
        email
    )

    return templates.TemplateResponse(
        request = request,
        name = "index.html"
    )
