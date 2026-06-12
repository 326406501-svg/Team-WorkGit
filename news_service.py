# קובץ השירות של החדשות
# אחראי על פנייה ל-New York Times API והחזרת כתבות

import requests

from fastapi import HTTPException


# מפתח הגישה ל-New York Times API
API_KEY = "cc7d0ca7426449c294450595f874aec6"


# רשימת הקטגוריות שהמערכת תומכת בהן לפי NYT Top Stories API
VALID_CATEGORIES = [
    "arts",
    "automobiles",
    "books",
    "business",
    "fashion",
    "food",
    "health",
    "home",
    "insider",
    "magazine",
    "movies",
    "nyregion",
    "obituaries",
    "opinion",
    "politics",
    "realestate",
    "science",
    "sports",
    "sundayreview",
    "technology",
    "theater",
    "t-magazine",
    "travel",
    "upshot",
    "us",
    "world"
]


# מוציא תמונה מתוך כתבה של NYT
def get_article_image(article):
    multimedia = article.get("multimedia")

    if multimedia:
        return multimedia[0].get("url")

    return None


# מסדר כתבה שחזרה מ-NYT למבנה אחיד שה-Frontend יבין
def format_article(article, category):
    return {
        "id": article.get("url"),
        "title": article.get("title"),
        "description": article.get("abstract"),
        "url": article.get("url"),
        "image": get_article_image(article),
        "source": "New York Times",
        "category": category
    }


# מביא כתבות לפי קטגוריה אחת
# amount קובע כמה כתבות להחזיר
def fetch_news_by_category(category, amount=10):
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code = 400,
            detail = "Invalid category"
        )

    url = f"https://api.nytimes.com/svc/topstories/v2/{category}.json"

    params = {
        "api-key": API_KEY
    }

    try:
        response = requests.get(url, params=params)

        response.raise_for_status()

        data = response.json()

        articles = []

        results = data.get("results")

        # אם אין כתבות בקטגוריה מסוימת, מחזירים רשימה ריקה ולא מפילים את השרת
        if results is None:
            return []

        # לוקחים רק את כמות הכתבות שביקשנו
        for article in results[:amount]:
            articles.append(
                format_article(article, category)
            )

        return articles

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code = 500,
            detail = "Failed to fetch news"
        )


# מביא כתבות ממספר קטגוריות
def fetch_news_by_multiple_categories(categories):
    all_articles = []

    # עוברים על כל קטגוריה ומוסיפים את הכתבות שלה לרשימה אחת
    for category in categories:
        articles = fetch_news_by_category(category)

        all_articles.extend(articles)

    return all_articles