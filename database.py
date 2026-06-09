# קובץ החיבור למסד הנתונים
# אחראי על התחברות ל-PostgreSQL
# ועל יצירת הטבלאות הראשוניות של הפרויקט

import psycopg2


# יצירת חיבור למסד הנתונים
connection = psycopg2.connect(
    host = "localhost",
    database = "news_db",
    user = "postgres",
    password = "Dallal007!"
)


# יצירת cursor שמאפשר להריץ פקודות SQL
cursor = connection.cursor()


# יצירת טבלת משתמשים אם היא עדיין לא קיימת
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role VARCHAR(20) DEFAULT 'user'
);
""")


# אם הטבלה כבר הייתה קיימת לפני שהוספנו email ו-role,
# הפקודות האלו מוסיפות את העמודות החסרות בלי למחוק מידע קיים
cursor.execute("""
ALTER TABLE users
ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE;
""")

cursor.execute("""
ALTER TABLE users
ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user';
""")


# יצירת טבלת תחומי עניין אם היא עדיין לא קיימת
cursor.execute("""
CREATE TABLE IF NOT EXISTS interests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL
);
""")


# שמירת השינויים במסד הנתונים
connection.commit()

print("Tables created successfully")


# סגירת החיבור למסד בצורה מסודרת
cursor.close()
connection.close()