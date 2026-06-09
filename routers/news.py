# קובץ ה-Router של החדשות
# אחראי על כל הכתובות שקשורות לחדשות

from fastapi import APIRouter

from news_service import (
    fetch_news_by_category,
    fetch_news_by_multiple_categories
)


# יצירת Router שכל הנתיבים שלו מתחילים ב-/news
router = APIRouter(
    prefix="/news",
    tags=["news"]
)


# מחזיר את כל הקטגוריות שהמערכת תומכת בהן
@router.get("/categories/list")
def get_categories():
    return {
        "categories": [
            "sports",
            "technology",
            "science",
            "business",
            "health"
        ]
    }


# מחזיר כתבות מכמה קטגוריות ביחד
# דוגמה:
# /news/multiple/categories?categories=sports,technology
@router.get("/multiple/categories")
def get_news_by_multiple_categories(categories: str):
    selected_categories = categories.split(",")

    articles = fetch_news_by_multiple_categories(selected_categories)

    return {
        "categories": selected_categories,
        "articles": articles
    }


# מחזיר כתבות לפי קטגוריה אחת
# דוגמה:
# /news/sports
@router.get("/{category}")
def get_news_by_category(category: str):
    articles = fetch_news_by_category(category)
    return {
        "category": category,
        "articles": articles
    }