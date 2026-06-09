# קובץ ראשי של הפרויקט
# אחראי על יצירת שרת FastAPI
# וחיבור כל ה-Routers של המערכת

from fastapi import FastAPI
from routers import news


# יצירת אפליקציית FastAPI
app = FastAPI()


# חיבור Router של החדשות
app.include_router(news.router)


# נתיב בדיקה ראשי
@app.get("/")
def home():
    return {
        "message": "News API is running"
    }