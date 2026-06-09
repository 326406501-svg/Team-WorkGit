#הרשמהfrom pydantic import   BaseModel
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
import json
# import jwt
import datetime
SECRET_KEY = "my_super_secret_key"
from intersects import get_status
from intersects import user_interests

def load_users(): 
    with open ("users.json","r",encoding="utf-8") as file:
        return json.load(file)

users=load_users()
#print(users)
#בדיקה מוצלחת

def  save_users(users):
    with open ("users.json","w",encoding="utf-8") as file:
        json.dump(users,file,indent=4,ensure_ascii=False)
#users=[{"id":1,"username":"guy"}]
#save_users(users)
#בדיקה מוצלחת

def get_next_id(users):
    max_id = max([user_data["id"] for user_data in users.values()], default=0)
    return max_id + 1

#print(get_next_id(users))
#בדיקה מוצלחת
@router.post('/register', response_class=HTMLResponse)
def register_user(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...), 
    email: str = Form(...)
):
    users = load_users()
    
    if username in users:
        # 1. Added request as the first argument
        return get_status( "Username already exists! Please choose another one.",request)
        
    elif len(password) < 6 or len(password) > 10:
        return get_status( "Invalid password! Must be between 6 and 10 characters.",request)
        
    elif any(user_data["email"] == email for user_data in users.values()):
        return get_status( "Email already exists! Please choose another one.",request)
        
    else:
        user_id = get_next_id(users)
        users[username] = {"id": user_id, "password": password, "email": email, "role": "user"}
        save_users(users)
        
        return templates.TemplateResponse(request=request, name="index.html")   


def login_user():
    users = load_users()
    username_input = input("Enter username to login: ")
    if username_input in users: 
        password_input = input("Enter password: ")
        if users[username_input]["password"] == password_input: 
            print(f"Login successful! Welcome back, {username_input}.")
            payload = {
                "user_id": users[username_input]["id"],
                "username": username_input,
                "role": users[username_input].get("role", "user"),  
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            print(f"Your JWT Token:\n{token}\n")
            return token
        else:
            print("Error: Incorrect password!")
    else:
        print("Error: Username does not exist!")

#login_user()
#בדיקה מוצלחת (שם משתמש קיים,סיסמה נכונה)
def delete_user_account(token):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_payload.get("role") == "admin":
            print(f"\n--- Access Granted (Admin: {decoded_payload['username']}) ---")
            users = load_users()
            user_to_delete = input("Enter username to delete: ")

            if user_to_delete in users:
                del users[user_to_delete]
                save_users(users)
                print(f"User '{user_to_delete}' has been deleted successfully.")
            else:
                print("Error: Username to delete does not exist.")
        else:         
            print("Access Denied! Only admins can perform this action.")
            
    except jwt.ExpiredSignatureError:
        print("Error: Your session has expired! Please login again.")
    except jwt.InvalidTokenError:
        print("Error: Invalid Token! Access blocked.")