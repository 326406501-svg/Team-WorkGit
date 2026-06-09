# מודלים של הנתונים במערכת
# מגדירים איזה מידע המשתמש שולח לשרת

from pydantic import BaseModel


# מודל להרשמת משתמש חדש
class UserRegister(BaseModel):
    username: str
    password: str


# מודל לבחירת תחום עניין
class Interest(BaseModel):
    category: str