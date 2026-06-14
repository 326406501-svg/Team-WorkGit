# קובץ היסטוריה ומועדפים
# אחראי על:
# 1. הצגת היסטוריית חיפושים של משתמש
# 2. שמירת כתבות במועדפים
# 3. מחיקת היסטוריה ומועדפים
# כל המידע נשמר ונשלף מ-PostgreSQL

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_database_connection
from news_service import fetch_news_by_category


router = APIRouter()

templates = Jinja2Templates(directory = "html")


# מחזיר עמוד סטטוס עם הודעה למשתמש
def get_status(status: str, request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "status.html",
        context = {
            "status_code": status
        }
    )


# מחזיר משתמש לפי שם משתמש
def get_user_by_username(username):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, password, email, role
        FROM users
        WHERE username = %s;
    """, (username,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


# מחזיר משתמש רק אם שם המשתמש והסיסמה נכונים
def get_user_by_username_and_password(username, password):
    user = get_user_by_username(username)

    if user is None:
        return None

    saved_password = user[2]

    if password != saved_password:
        return None

    return user


# שומר חיפוש של משתמש בטבלת history
def user_interests(username, interest_category):
    user = get_user_by_username(username)

    if user is None:
        return

    user_id = user[0]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO history (user_id, article_title, article_url, category)
        VALUES (%s, %s, %s, %s);
    """, (
        user_id,
        "Search",
        "Search action",
        interest_category
    ))

    connection.commit()

    cursor.close()
    connection.close()


# בונה מבנה שמתאים ל-user_history.html
def build_user_profile(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, viewed_at
        FROM history
        WHERE user_id = %s
        ORDER BY viewed_at DESC;
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    user_profile = {}

    for row in rows:
        category = row[0]
        viewed_at = str(row[1])

        if category not in user_profile:
            user_profile[category] = {
                "date_of_search": [],
                "total time of search": 0
            }

        user_profile[category]["date_of_search"].append(viewed_at)
        user_profile[category]["total time of search"] += 1

    return user_profile


# בונה מבנה של כתבות שמורות שמתאים ל-user_history.html
def build_saved_posts(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, url, image
        FROM favorites
        WHERE user_id = %s
        ORDER BY id DESC;
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    save_posts = {}

    for row in rows:
        title = row[0]
        url = row[1]
        image = row[2]

        save_posts[title] = {
            "description": image if image else "Saved article",
            "url": url
        }

    return save_posts


# מחזיר כתבות לפי החיפוש הכי נפוץ של המשתמש
def show_users_favorite_posts(username):
    user = get_user_by_username(username)

    if user is None:
        return []

    user_id = user[0]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, COUNT(*) AS total_searches
        FROM history
        WHERE user_id = %s
        GROUP BY category
        ORDER BY total_searches DESC
        LIMIT 1;
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return []

    most_frequent_topic = row[0]

    return fetch_news_by_category(most_frequent_topic, 3)


# הצגת ההיסטוריה והמועדפים של המשתמש
@router.post("/data", response_class=HTMLResponse)
def show_data_in_html(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_username_and_password(username, password)

    if user is None:
        return get_status(
            "invalid username or password",
            request
        )

    user_id = user[0]

    user_profile = build_user_profile(user_id)
    save_posts = build_saved_posts(user_id)
    favorite_posts = show_users_favorite_posts(username)

    return templates.TemplateResponse(
        request = request,
        name = "user_history.html",
        context = {
            "username": username,
            "user_profile": user_profile,
            "save_posts": save_posts,
            "password": password,
            "favorite_posts": favorite_posts
        }
    )


# שמירת כתבה במועדפים
@router.post("/data_save")
def save_data_in_html(
    username: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    url: str = Form(...)
):
    user = get_user_by_username(username)

    if user is None:
        return {
            "message": "invalid username"
        }

    user_id = user[0]

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
        url,
        title,
        url,
        description,
        "New York Times",
        None
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "post saved successfully"
    }


# עמוד login מחזיר כרגע את index.html לפי המבנה של אלעד
@router.get("/login", response_class=HTMLResponse)
def show_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "index.html"
    )


# מחיקת היסטוריה ומועדפים של משתמש
@router.post("/cleanhistory")
def clean_history(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_username_and_password(username, password)

    if user is None:
        return get_status(
            "invalid username or password",
            request
        )

    user_id = user[0]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM history
        WHERE user_id = %s;
    """, (user_id,))

    cursor.execute("""
        DELETE FROM favorites
        WHERE user_id = %s;
    """, (user_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return show_data_in_html(
        request = request,
        username = username,
        password = password
    )