import requests
from fastapi import HTTPException

API_KEY = "cc7d0ca7426449c294450595f874aec6"

VALID_CATEGORIES = [
    "sports",
    "technology",
    "science",
    "business",
    "health"
]


def fetch_news_by_category(category):
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail="Invalid category"
        )

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "apiKey": API_KEY,
        "category": category,
        "language": "en",
        "pageSize": 10
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles = []

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


def fetch_news_by_multiple_categories(categories):
    all_articles = []

    for category in categories:
        articles = fetch_news_by_category(category)
        all_articles.extend(articles)

    return all_articles