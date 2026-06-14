from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers.intersects import router as intersects_router
from routers.users import router as register_router
from Eshow_users_search import router as show_users_search
from routers.admin import router as admin_router

from news_service import fetch_news_by_category


app = FastAPI()


# CSS
app.mount(
    "/css",
    StaticFiles(directory = "css"),
    name = "css"
)

app.mount(
    "/js",
    StaticFiles(directory = "js"),
    name = "js"
)

# HTML
templates = Jinja2Templates(directory = "html")


# Routers
app.include_router(intersects_router)
app.include_router(show_users_search)
app.include_router(register_router)
app.include_router(admin_router)


# Home Page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    data = fetch_news_by_category("politics", 3)

    return templates.TemplateResponse(
        request = request,
        name = "register.html",
        context = {
            "data": data
        }
    )