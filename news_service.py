import requests
from fastapi import HTTPException

API_KEY = "0ujXTZFKIPFM92nK0MaKblLrkrFL8bxRUIiG4FBgGkGE5Mpt"

VALID_CATEGORIES = [
    "arts", "automobiles", "books", "business", "fashion", "food",
    "health", "home", "insider", "magazine", "movies", "nyregion",
    "obituaries", "opinion", "politics", "realestate", "science",
    "sports", "sundayreview", "technology", "theater", "t-magazine",
    "travel", "upshot", "us", "world"
]


def get_article_image(article):
    multimedia = article.get("multimedia")
    if multimedia and isinstance(multimedia, list) and len(multimedia) > 0:
        for media_item in multimedia:
            if isinstance(media_item, dict) and media_item.get("url"):
                return media_item.get("url")
    return None


def fetch_news_by_category(category,x=10):
    
    category_clean = category.lower().strip() if category else "world"

    if category_clean not in VALID_CATEGORIES:
        category_clean = "world"

    url = f"https://api.nytimes.com/svc/topstories/v2/{category_clean}.json"

    params = {
        "api-key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data is None or not isinstance(data, dict):
            return []

        articles = []
        results_list = data.get("results", [])
        
        if not isinstance(results_list, list):
            return []

        for article in results_list:
            if not article or not isinstance(article, dict):
                continue
                
            articles.append({
                "title": article.get("title"),
                "description": article.get("abstract"),
                "url": article.get("url"),
                "image": get_article_image(article),
                "source": "New York Times",  
                "category": category_clean
            })

        return articles[:x]

    except requests.exceptions.RequestException:
        return []

