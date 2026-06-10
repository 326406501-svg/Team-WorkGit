# קובץ משתמשים
# אחראי על הרשמה, התחברות ושליפת פרטי המשתמש המחובר

from fastapi import APIRouter, HTTPException, Depends

from database import get_database_connection
from models import UserRegister, UserLogin
from auth_service import create_token, get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# הרשמת משתמש חדש
@router.post("/register")
def register_user(user: UserRegister):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = %s OR email = %s;
    """, (user.username, user.email))

    existing_user = cursor.fetchone()

    if existing_user is not None:
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    cursor.execute("""
        INSERT INTO users (username, password, email, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (user.username, user.password, user.email, "user"))

    new_user_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User registered successfully",
        "user_id": new_user_id
    }


# התחברות משתמש וקבלת JWT
@router.post("/login")
def login_user(user: UserLogin):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username, password, role
        FROM users
        WHERE username = %s;
    """, (user.username,))

    existing_user = cursor.fetchone()

    cursor.close()
    connection.close()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="Username does not exist"
        )

    user_id = existing_user[0]
    username = existing_user[1]
    saved_password = existing_user[2]
    role = existing_user[3]

    if user.password != saved_password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    token = create_token(
        user_id=user_id,
        username=username,
        role=role
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }


# בדיקת המשתמש המחובר לפי JWT
@router.get("/me")
def get_my_user(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "role": current_user["role"]
    }