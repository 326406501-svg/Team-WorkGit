from pydantic import   BaseModel
from fastapi import APIRouter,FastAPI, Form, Depends,Request
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
def create_json_intersets_file():
 with open(r'intersects.json' ,'w') as file :
    json.dump({},file)


def read_json_intersets_file():
 with open(r'intersects.json' ,'r') as file :
    return json.load(file)

def write_to_json_file(x):
  with open(r'intersects.json' ,'w') as file :
    json.dump(x,file)
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