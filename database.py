import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="news_db",
    user="postgres",
    password="Dallal007!"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS interests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL
);
""")

connection.commit()

print("Tables created successfully")

cursor.close()
connection.close()