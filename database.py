# קובץ החיבור למסד הנתונים
# אחראי על התחברות ל-PostgreSQL ועל יצירת כל הטבלאות

import psycopg2


# פונקציה שמחזירה חיבור למסד הנתונים
def get_database_connection():
    connection = psycopg2.connect(
        host = "localhost",
        database = "news_db",
        user = "postgres",
        password = "Dallal007!"
    )

    return connection


# פונקציה שיוצרת את כל הטבלאות של הפרויקט
def create_tables():
    connection = get_database_connection()
    cursor = connection.cursor()

    # טבלת משתמשים
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        role VARCHAR(20) DEFAULT 'user'
    );
    """)

    # טבלת תחומי עניין
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interests (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        category VARCHAR(50) NOT NULL
    );
    """)

    # טבלת מועדפים
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        article_id TEXT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        image TEXT,
        source VARCHAR(100),
        category VARCHAR(50)
    );
    """)

    # אם טבלת favorites כבר הייתה קיימת לפני שהוספנו article_id,
    # הפקודה הזאת מוסיפה את העמודה בלי למחוק מידע קיים
    cursor.execute("""
    ALTER TABLE favorites
    ADD COLUMN IF NOT EXISTS article_id TEXT;
    """)

    # טבלת תגובות
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        article_url TEXT NOT NULL,
        comment_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # טבלת היסטוריית צפייה
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        article_title TEXT NOT NULL,
        article_url TEXT NOT NULL,
        category VARCHAR(50),
        viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    connection.commit()

    cursor.close()
    connection.close()

    print("Tables created successfully")


# הפעלת יצירת הטבלאות רק כאשר מריצים את הקובץ ישירות
if __name__ == "__main__":
    create_tables()