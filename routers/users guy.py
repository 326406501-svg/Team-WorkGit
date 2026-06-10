# קובץ JWT
# אחראי על יצירת Token ופענוח Token

import jwt
import datetime

from fastapi import HTTPException


SECRET_KEY = "my_super_secret_key"

ALGORITHM = "HS256"


# יצירת JWT למשתמש שהתחבר
def create_token(user_id, username, role):

    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": (
            datetime.datetime.now(
                datetime.timezone.utc
            )
            + datetime.timedelta(hours = 1)
        )
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm = ALGORITHM
    )

    return token


# פענוח JWT
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