#הרשמה והתחברות
#שם  משתמש,סיסמה,גימייל
import json
import jwt
import datetime
SECRET_KEY = "my_super_secret_key"
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

def register_user():
    users=load_users()
    while True:
        username = input("enter username: ")
        if username in users:
            print("Username already exists! Please choose another one.")
        else:
            break  
    while True:
        password = input("enter password (6-10 characters): ")
        if 6 <= len(password) <= 10:
            break
        else:  
            print("Invalid password! Must be between 6 and 10 characters.")
    while True:
        email = input("enter email: ")
        if any(user_data["email"] == email for user_data in users.values()):
            print("Email already exists! Please choose another one.")
        else:
            break   

    user_id=get_next_id(users)
    users[username] = {"id": user_id,"password": password,"email": email,"role":"user"}
    save_users(users)
    print("User registered successfully")

register_user()
#בדיקה מוצלחת(שולל שם משתמש זהה,סיסמה שהיא לא בין 6-10 תווים ושולל גימייל שונה)

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