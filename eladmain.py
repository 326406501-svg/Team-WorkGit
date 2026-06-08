import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from intersects import router as intersects_router
import uvicorn
app = FastAPI()

templates = Jinja2Templates(directory=r'C:\Users\Z\news-project\staticGit')
app.include_router(intersects_router)
app.mount("/staticGit",StaticFiles(directory=r'C:\Users\Z\news-project\staticGit'),name="staticGit")
@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
  return templates.TemplateResponse(
          request=request, 
          name="open.html" )
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)