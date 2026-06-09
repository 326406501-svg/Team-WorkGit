import json
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status,FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
#import uuid – מייצר איי די יחודי לתגובה שנכתבה
#HTTPBearer-נעילה שרק משתמשים רשומים/אדמינים יכולים לקבל הרשאה לכתיבת תגובות
#HTTPAuthorizationCredentials- מזהה אם מדובר בטוקן של  משתמש רגיל או אדמיןבהמשך כרגע שולח את הטוקן מהרשת חזרה לפייתון 
#from pydantic import BaseModel-(class) לא למדנו אבל דואג שהמידע יעבור בתצורה מסויימת
router = APIRouter(prefix="/comments", tags=["comments"])
COMMENTS_FILE = "comments.json"
security = HTTPBearer()
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"

class CommentModel(BaseModel):
    article_id: str 
    content: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # תרגום מחרוזת הטוקן הארוכה מהבקשה שהגיעה מהרשת
    token = credentials.credentials
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_payload.get("username")
        role = decoded_payload.get("role", "user")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="username is not found")
        return {"username": username, "role": role}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token expired! pls sign in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token is wrong,access denied")
def read_comments():
    if not os.path.exists(COMMENTS_FILE):
        return {}  
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
def write_comments(comments):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)

# פעולת הוספת תגובה (רק למשתמשים מחוברים - שם המשתמש נלקח ישירות מהטוקן האמיתי שלהם!)
@router.post("/add")
def add_comment(comment: CommentModel, current_user: dict = Depends(get_current_user)):
    comments_db = read_comments()
    comment_id = str(uuid.uuid4())[:8]
    comments_db[comment_id] = {"article_id": comment.article_id,"username": current_user["username"],              
    "content": comment.content,"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}    
    write_comments(comments_db)    
    return {"message": "comment published!", "comment_id": comment_id}

# פעולת שליפת תגובות לפי מזהה כתבה (פתוח לכולם - לא דורש טוקן אבטחה)
@router.get("/{article_id}")
def get_comments(article_id: str):
    comments_db = read_comments()
    filtered_comments = {
        cid: cdata for cid, cdata in comments_db.items() 
        if cdata["article_id"] == article_id}
    
    return {"article_id": article_id, "comments": filtered_comments}
#cid (קיצור של Comment ID) 
#חלוקה של תגובות ומאגר הכתובות וסינון שלהן לכל מאמר
@router.delete("/delete/{comment_id}")
def delete_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied! Only administrators are allowed to delete comments."
        )
    comments_db = read_comments()
    if comment_id not in comments_db:
        raise HTTPException(status_code=404, detail="Comment not found.")
        
    del comments_db[comment_id]
    write_comments(comments_db)
    
    return {"message": f"Comment {comment_id} deleted successfully by admin."}


#מחובר לעצמו כשרת איי פי איי כי אני לא רוצה לגעת בראשי כי הוא בטוח עבר שינויים ואני עושה לו בדיקה
app = FastAPI(title="בדיקת ראוטר תגובות")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("comments_router:app", host="127.0.0.1", port=8000, reload=True)