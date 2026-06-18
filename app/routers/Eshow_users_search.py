# ×§×•×‘×¥ ×—×™×¤×•×© ×›×ª×‘×•×ª
# ××—×¨××™ ×¢×œ:
# 1. ×—×™×¤×•×© ×›×ª×‘×•×ª ×œ×¤×™ ×§×˜×’×•×¨×™×”
# 2. ×”×¦×’×ª ×¢×•×“ ×›×ª×‘×•×ª ×›××©×¨ ×”×ž×©×ª×ž×© ×œ×•×—×¥ See more posts
# 3. ×”×•×¡×¤×ª ×ª×’×•×‘×•×ª ×œ×›×ª×‘×•×ª
# 4. ×©×œ×™×¤×ª ×ª×’×•×‘×•×ª ×§×™×™×ž×•×ª ×œ×›×œ ×›×ª×‘×”

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.paths import TEMPLATES_DIR
from app.database import get_database_connection
from app.services.news_service import fetch_news_by_category
from app.routers.intersects import (
    get_user_by_username,
    get_status,
    user_interests
)


router = APIRouter()

templates = Jinja2Templates(directory = TEMPLATES_DIR)


# ×©×œ×™×¤×ª ×ª×’×•×‘×•×ª ×©×œ ×›×ª×‘×” ×œ×¤×™ URL
def get_comments_for_article(article_url):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT users.username, comments.comment_text, comments.created_at
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
            "username": row[0],
            "comment_text": row[1],
            "created_at": row[2]
        })

    return comments


# ×ž×•×¡×™×£ ×œ×›×œ ×›×ª×‘×” ××ª ×”×ª×’×•×‘×•×ª ×©×œ×”
def attach_comments_to_articles(articles):
    for article in articles:
        article["comments"] = get_comments_for_article(article["url"])

    return articles


# ×—×™×¤×•×© ×›×ª×‘×•×ª ×œ×¤×™ ×§×˜×’×•×¨×™×”
@router.post("/search_user", response_class=HTMLResponse)
def show_user_search(
    request: Request,
    username: str = Form(...),
    category: str = Form(...)
):
    user = get_user_by_username(username)

    if user is None:
        return get_status(
            "invalid username",
            request
        )

    user_interests(username, category)

    data = fetch_news_by_category(category)
    data = attach_comments_to_articles(data)

    return templates.TemplateResponse(
        request = request,
        name = "Euser_search.html",
        context = {
            "username": username,
            "data": data
        }
    )


# ×”×¦×’×ª ×¢×•×“ ×›×ª×‘×•×ª ×ž××•×ª×” ×§×˜×’×•×¨×™×”
@router.post("/search_user_more", response_class=HTMLResponse)
def show_user_search_more(
    request: Request,
    username: str = Form(...),
    category: str = Form(...),
    amount: int = Form(...)
):
    user = get_user_by_username(username)

    if user is None:
        return get_status(
            "invalid username",
            request
        )

    user_interests(username, category)

    data = fetch_news_by_category(
        category,
        amount + 10
    )

    data = attach_comments_to_articles(data)

    return templates.TemplateResponse(
        request = request,
        name = "Euser_search.html",
        context = {
            "username": username,
            "data": data
        }
    )


# ×”×•×¡×¤×ª ×ª×’×•×‘×” ×œ×›×ª×‘×”
@router.post("/add_comment", response_class=HTMLResponse)
def add_comment(
    request: Request,
    username: str = Form(...),
    article_url: str = Form(...),
    comment_text: str = Form(...),
    category: str = Form(...)
):
    user = get_user_by_username(username)

    if user is None:
        return get_status(
            "invalid username",
            request
        )

    user_id = user[0]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO comments (user_id, article_url, comment_text)
        VALUES (%s, %s, %s);
    """, (
        user_id,
        article_url,
        comment_text
    ))

    connection.commit()

    cursor.close()
    connection.close()

    data = fetch_news_by_category(category)
    data = attach_comments_to_articles(data)

    return templates.TemplateResponse(
        request = request,
        name = "Euser_search.html",
        context = {
            "username": username,
            "data": data
        }
    )
