import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from intersects import router as intersects_router
from Eshow_users_search import router as show_users_search
import uvicorn
from news_service import fetch_news_by_category
from users import router as register_router
app = FastAPI()
app.mount("/static", StaticFiles(directory=r"C:\Users\Z\Documents\Team-git-project\Team-WorkGit\staticGit"), name="staticGit")
templates = Jinja2Templates(directory=r'C:\Users\Z\Documents\Team-git-project\Team-WorkGit\staticGit')
app.include_router(intersects_router)
app.include_router(show_users_search)
app.include_router(register_router)
app.mount("/staticGit",StaticFiles(directory=r'C:\Users\Z\Documents\Team-git-project\Team-WorkGit\staticGit'),name="staticGit")

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
  data=fetch_news_by_category("politics",3)
  return templates.TemplateResponse(
          request=request, 
          name="register.html",
           context={"data":data} )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)