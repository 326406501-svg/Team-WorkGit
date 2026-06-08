from fastapi import FastAPI
from routers import news

app = FastAPI()

app.include_router(news.router)

@app.get("/")
def home():
    return {"message": "News API is running"}