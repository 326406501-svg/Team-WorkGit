# קובץ משתמשים
# אחראי על הרשמת משתמשים חדשים מתוך register.html
# במקום לשמור ב-users.json, אנחנו שומרים בטבלת users ב-PostgreSQL

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_database_connection
from intersects import get_status


router = APIRouter()

templates = Jinja2Templates(directory="staticGit")


# הרשמת משתמש חדש
# מקבל username, password, email מהטופס של register.html
@router.post("/register", response_class = HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    connection = get_database_connection()
    cursor = connection.cursor()

    # בדיקה אם username או email כבר קיימים במסד הנתונים
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

    # בדיקת אורך סיסמה
    if len(password) < 6 or len(password) > 10:
        cursor.close()
        connection.close()

        return get_status(
            "Invalid password! Must be between 6 and 10 characters.",
            request
        )

    # הכנסת המשתמש החדש לטבלת users
    cursor.execute("""
        INSERT INTO users (username, password, email, role)
        VALUES (%s, %s, %s, %s);
    """, (username, password, email, "user"))

    connection.commit()

    cursor.close()
    connection.close()

    return templates.TemplateResponse(
        request = request,
        name = "index.html"
    )