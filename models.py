# מודלים של הנתונים במערכת
# מגדירים איזה מידע המשתמש שולח לשרת

from pydantic import BaseModel


# מודל להרשמת משתמש חדש
class UserRegister(BaseModel):
    username: str
    password: str
    email: str


# מודל להתחברות משתמש
class UserLogin(BaseModel):
    username: str
    password: str


# מודל לבחירת תחום עניין
class Interest(BaseModel):
    category: str


# מודל לשמירת כתבה במועדפים
class FavoriteArticle(BaseModel):
    title: str
    url: str
    image: str | None = None
    source: str | None = None
    category: str | None = None


# מודל להוספת תגובה
class CommentCreate(BaseModel):
    article_url: str
    comment_text: str


# מודל להיסטוריית צפייה
class HistoryCreate(BaseModel):
    article_title: str
    article_url: str
    category: str | None = None