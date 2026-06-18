# קובץ message.py
# אחראי על שליחת מיילים דרך Gmail

import smtplib
from email.mime.text import MIMEText


# כתובת הג'ימייל שממנה יישלחו המיילים
GMAIL_ADDRESS = "326406501@ziv-school.com"

# App Password של גוגל (לא הסיסמה הרגילה)
GMAIL_APP_PASSWORD = "hmmn mwuh jpbg eahl"  


# פונקציה כללית לשליחת מייל
def send_email(to_email, subject, body):

    # יצירת תוכן המייל
    message = MIMEText(body, "plain", "utf-8")

    # כותרת המייל
    message["Subject"] = subject

    # מי שולח
    message["From"] = GMAIL_ADDRESS

    # למי שולחים
    message["To"] = to_email

    # התחברות לשרת של Gmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        # התחברות לחשבון
        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        # שליחת המייל
        server.send_message(message)


# שליחת מייל הרשמה למשתמש חדש
def send_welcome_email(username, email):

    subject = "Welcome to Daily News Hub"

    body = f"""
Dear {username},

Thank you for joining Daily News Hub!

Your account has been successfully created and you can now start exploring the latest news from around the world.

Account Details:

• Username: {username}
• Email: {email}

What you can do now:

✓ Browse the latest news by category
✓ Save articles for later reading
✓ Track your search history
✓ Discover personalized content

We are excited to have you as part of our community.

Best regards,

The Daily News Hub Team
"""

    # שליחת המייל
    send_email(
        email,
        subject,
        body
    )


# שליחת מייל עם עדכוני חדשות
def send_news_update_email(
    username,
    email,
    articles
):

    subject = "New Stories Are Waiting For You"

    article_titles = ""

    # הכנסת 3 כתבות ראשונות למייל
    for article in articles[:3]:

        article_titles += (
            f"• {article['title']}\n"
        )

    body = f"""
Hello {username},

Fresh news has just arrived on Daily News Hub.

Here are some of today's highlights:

{article_titles}

Stay informed with the latest updates from around the world.

See you there!

The Daily News Hub Team
"""

    # שליחת המייל
    send_email(
        email,
        subject,
        body
    )
    # from_email = "326406501@ziv-school.com" 
    # password = "hmmn mwuh jpbg eahl"   