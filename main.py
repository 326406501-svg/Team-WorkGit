# קובץ ראשי של הפרויקט
# אחראי על יצירת שרת FastAPI וחיבור כל ה-Routers

from fastapi import FastAPI

from routers import news
from routers import users
from routers import interests
from routers import favorites
from routers import comments
from routers import admin


# יצירת אפליקציית FastAPI
app = FastAPI(
    title="News Summary Project",
    description="Guest, User and Admin news system",
    version="1.0.0"
)


# חיבור כל חלקי המערכת
app.include_router(news.router)
app.include_router(users.router)
app.include_router(interests.router)
app.include_router(favorites.router)
app.include_router(comments.router)
app.include_router(admin.router)


# נתיב בדיקה ראשי
@app.get("/")
def home():
    return {
        "message": "News Summary API is running"
    }