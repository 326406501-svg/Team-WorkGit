from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.paths import STATIC_DIR, TEMPLATES_DIR
from app.routers.intersects import router as intersects_router
from app.routers.users import router as register_router
from app.routers.Eshow_users_search import router as show_users_search
from app.routers.admin import router as admin_router

from app.services.news_service import fetch_news_by_category


app = FastAPI()


app.mount(
    "/css",
    StaticFiles(directory = STATIC_DIR / "css"),
    name = "css"
)

app.mount(
    "/js",
    StaticFiles(directory = STATIC_DIR / "js"),
    name = "js"
)

app.mount(
    "/static",
    StaticFiles(directory = STATIC_DIR),
    name = "static"
)

# HTML
templates = Jinja2Templates(directory = TEMPLATES_DIR)


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
