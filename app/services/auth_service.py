# קובץ שאחראי על JWT
# יוצר token, מפענח token ומזהה את המשתמש המחובר

import jwt
import datetime

from fastapi import HTTPException, Header


# חייב להיות זהה בכל המערכת
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"


# יצירת token אחרי התחברות מוצלחת
def create_token(user_id, username, role):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

    return token


# פענוח token
def decode_token(token):
    try:
        user_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )

        return user_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = 401,
            detail = "Token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid token"
        )


# קבלת המשתמש המחובר מתוך Header
def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(
            status_code = 401,
            detail="Missing Authorization header"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code = 401,
            detail="Invalid Authorization format"
        )

    token = authorization.replace("Bearer ", "")

    user_data = decode_token(token)

    return user_data


# בדיקה שהמשתמש הוא admin
def require_admin(user_data):
    if user_data.get("role") != "admin":
        raise HTTPException(
            status_code = 403,
            detail = "Admin permission required"
        )