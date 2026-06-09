# קובץ השירות של החדשות
# אחראי על פנייה ל-NewsAPI והחזרת כתבות

import requests
from fastapi import HTTPException


# מפתח הגישה ל-NewsAPI
API_KEY = "cc7d0ca7426449c294450595f874aec6"


# רשימת הקטגוריות שהמערכת תומכת בהן
VALID_CATEGORIES = [
    "sports",
    "technology",
    "science",
    "business",
    "health"
]


# מביא כתבות לפי קטגוריה אחת
def fetch_news_by_category(category):

    # בדיקה שהקטגוריה חוקית
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail="Invalid category"
        )

    # כתובת ה-API
    url = "https://newsapi.org/v2/top-headlines"

    # הפרמטרים שנשלחים ל-NewsAPI
    params = {
        "apiKey": API_KEY,
        "category": category,
        "language": "en",
        "pageSize": 10
    }

    try:
        # שליחת בקשה ל-NewsAPI
        response = requests.get(url, params=params)

        # זריקת שגיאה במקרה של כישלון
        response.raise_for_status()

        # המרת התשובה ל-JSON
        data = response.json()

        # רשימת הכתבות שנחזיר למשתמש
        articles = []

        # data מכיל את כל המידע שחזר מה-API
        # כאן אנחנו עוברים על כל כתבה בנפרד כדי לקחת ממנה את המידע שאנחנו צריכים
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "image": article.get("urlToImage"),
                "source": article.get("source", {}).get("name"),
                "category": category
            })

        return articles

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch news"
        )


# מביא כתבות ממספר קטגוריות
def fetch_news_by_multiple_categories(categories):

    # רשימת כל הכתבות שנאסוף
    all_articles = []

    # מעבר על כל הקטגוריות
    for category in categories:
        articles = fetch_news_by_category(category)

        # הוספת הכתבות לרשימה אחת גדולה
        all_articles.extend(articles)

    return all_articles