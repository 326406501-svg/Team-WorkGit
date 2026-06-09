from pydantic import   BaseModel
from fastapi import APIRouter,FastAPI, Form, Depends,Request
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
from news_service import fetch_news_by_category
router = APIRouter()
templates = Jinja2Templates(directory=r'C:\Users\Z\Documents\Team-git-project\Team-WorkGit\staticGit')

def create_json_intersets_file():
 with open(r'intersects.json' ,'w') as file :
    json.dump({},file)


def read_json_intersets_file():
 with open(r'intersects.json' ,'r') as file :
    return json.load(file)

def write_to_json_file(x):
  with open(r'intersects.json' ,'w') as file :
    json.dump(x,file)

#save file in json
def create_json_save__post_file():
 with open(r'save_post.json' ,'w') as file :
    json.dump({},file)

def read_json_save__post_file():
 with open(r'save_post.json' ,'r') as file :
   return  json.load(file)
def write_to_save_post_file(x):
  with open(r'save_post.json' ,'w') as file :
    json.dump(x,file)
#get_uesers_password
def get_uesers_password_and_username():
 with open(r'C:\Users\Z\Documents\Team-git-project\Team-WorkGit\users.json' ,'r') as file :
   return  json.load(file)

def user_interests(username,interest_category):
    
    list_of_users=read_json_intersets_file()
    current_time_str = datetime.now().isoformat()
    #if its the first time of the user to connect
    if username not in  list_of_users :
     list_of_users[username]={interest_category:{
                    'date_of_search':[current_time_str],
                              "total time of search":1 }}
  
     write_to_json_file(list_of_users)
    else:
      user_profile=list_of_users[username]
      if interest_category in list_of_users[username].keys() :
        list_of_dates_connection=user_profile[interest_category]['date_of_search']
        #adding the  last time he search this topic
        list_of_dates_connection.append(current_time_str)
        #updating the amount of times he search this topic
        user_profile[interest_category]['total time of search']+=1
 
      # if its first time the user search this specific topic:
      else:user_profile[interest_category]={ 'date_of_search':[current_time_str],
                              "total time of search":1 }
      list_of_users[username]=user_profile
      write_to_json_file(list_of_users)
user_interests("tomer","sport")

@router.post("/data",response_class=HTMLResponse)
def show_data_in_html (request:Request,username:str = Form(...),password:int = Form(...)):
    list_of_users=get_uesers_password_and_username()
    if username in list_of_users and list_of_users[username]["password"]==password:
     data=read_json_intersets_file()
     save_posts=read_json_save__post_file()
     user_profile = data.get(username, {})
     user_posts = save_posts.get(username, {}) 
     return templates.TemplateResponse(
          request=request, 
          name="user_history.html", 
          context={"username":username,"user_profile": user_profile,"save_posts": user_posts})
    else:
      return get_status("invalid username or password",request)
@router.post("/data_save")
def save_data_in_html (username:str = Form(...), title:str = Form(...),description:str= Form(...)):
     list_of_users=read_json_save__post_file()
     if username not in list_of_users:
       list_of_users[username]={
         title:description
       }
     else:
           user_profile=list_of_users[username]
           user_profile[title]=description
     write_to_save_post_file(list_of_users)

def get_status(status:str,request:Request):
     return templates.TemplateResponse(
          request=request, 
          name="status.html", 
          context={"status_code":status})

@router.get("/login", response_class=HTMLResponse)
def show_login_page(request: Request):
    # 2. הכתובת /login תציג את הדף הישן שלך
    return templates.TemplateResponse(request=request, name="index.html")