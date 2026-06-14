# קובץ מיילים
# כרגע מדפיס מיילים לטרמינל
# בעתיד נחבר אותו ל-Gmail אמיתי

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

If you have any questions or need assistance, feel free to contact our support team.

Best regards,

The Daily News Hub Team
"""

    print("----- EMAIL PREVIEW -----")
    print("To:", email)
    print("Subject:", subject)
    print(body)
    print("-------------------------")


def send_news_update_email(username, email, articles):
    subject = "New Stories Are Waiting For You"

    article_titles = ""

    for article in articles[:3]:
        article_titles += f"• {article['title']}\n"

    body = f"""
Hello {username},

Fresh news has just arrived on Daily News Hub.

Here are some of today's highlights:

{article_titles}

Stay informed with the latest updates in:

✓ Politics
✓ Technology
✓ Science
✓ Sports
✓ Business

Visit Daily News Hub and discover what's happening around the world.

See you there!

The Daily News Hub Team
"""

    print("----- NEWS UPDATE EMAIL PREVIEW -----")
    print("To:", email)
    print("Subject:", subject)
    print(body)
    print("-------------------------------------")