from pydantic import   BaseModel
from fastapi import APIRouter,FastAPI, Form, Depends,Request
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
from news_service import fetch_news_by_category
from intersects import user_interests
router = APIRouter()
templates = Jinja2Templates(directory=r'C:\Users\Z\Documents\Team-git-project\Team-WorkGit\staticGit')
from news_service import fetch_news_by_category


@router.post("/search_user",response_class=HTMLResponse)
def show_user_search(request:Request,username:str = Form(...),category:str = Form(...)):
  #save the user 
  user_interests(username,category)
  data=fetch_news_by_category(category)
  return templates.TemplateResponse(
          request=request, 
          name="Euser_search.html", 
          context={"username":username,"data":data})





