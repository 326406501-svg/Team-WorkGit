# קובץ ה-Router של החדשות
# אחראי על כתבות לאורחים, משתמשים רשומים וחדשות לפי תחומי עניין

from fastapi import APIRouter, Depends

from database import get_database_connection
from auth_service import get_current_user
from news_service import (
    VALID_CATEGORIES,
    fetch_news_by_category,
    fetch_news_by_multiple_categories
)


router = APIRouter(
    prefix="/news",
    tags=["news"]
)


# חדשות גנריות לאורחים
@router.get("/guest")
def get_guest_news():
    articles = fetch_news_by_category("business")

    return {
        "mode": "guest",
        "message": "Generic guest news",
        "articles": articles
    }


# רשימת קטגוריות
@router.get("/categories/list")
def get_categories():
    return {
        "categories": VALID_CATEGORIES
    }


# חדשות מכמה קטגוריות ביחד
@router.get("/multiple/categories")
def get_news_by_multiple_categories(categories: str):
    selected_categories = categories.split(",")

    articles = fetch_news_by_multiple_categories(selected_categories)

    return {
        "categories": selected_categories,
        "articles": articles
    }


# חדשות מותאמות למשתמש רשום לפי תחומי עניין מה-DB
@router.get("/personal/me")
def get_personal_news(current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category
        FROM interests
        WHERE user_id = %s;
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    categories = [row[0] for row in rows]

    if len(categories) == 0:
        categories = ["business"]

    articles = fetch_news_by_multiple_categories(categories)

    return {
        "user_id": user_id,
        "categories": categories,
        "articles": articles
    }


# חדשות לפי קטגוריה אחת
@router.get("/{category}")
def get_news_by_category(category: str):
    articles = fetch_news_by_category(category)

    return {
        "category": category,
        "articles": articles
    }