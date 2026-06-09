# קובץ שאחראי על פענוח JWT
# המטרה: לזהות מי המשתמש המחובר לפי ה-token שגיא יוצר

import jwt
from fastapi import HTTPException


SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"


def decode_token(token):
    # מנסה לפענח את ה-token שקיבלנו מהמשתמש
    try:
        user_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return user_data

    # אם הזמן של ה-token נגמר
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    # אם ה-token לא תקין
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )