from fastapi import APIRouter
from news_service import fetch_news_by_category, fetch_news_by_multiple_categories

router = APIRouter(prefix="/news", tags=["news"])


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


@router.get("/multiple/categories")
def get_news_by_multiple_categories(categories: str):
    categories_list = categories.split(",")

    articles = fetch_news_by_multiple_categories(categories_list)

    return {
        "categories": categories_list,
        "articles": articles
    }


@router.get("/{category}")
def get_news_by_category(category: str):
    articles = fetch_news_by_category(category)

    return {
        "category": category,
        "articles": articles
    }