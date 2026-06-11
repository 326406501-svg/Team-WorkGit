import json
import smtplib
from email.mime.text import MIMEText

def send_customer_emails_from_json(name):
    # הגדרות המייל של העסק שלך
    from_email = "326406501@ziv-school.com"  # המייל שלך
    password = "hmmn mwuh jpbg eahl"             # סיסמת האפליקציה בת 16 האותיות מגוגל

    # 1. פתיחת קובץ ה-JSON וטעינת הנתונים
    with open('users.json', 'r', encoding='utf-8') as file:
        customers = json.load(file)  
    # 2. התחברות חד-פעמית לשרת של גוגל
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:          
            server.login(from_email, password)
            customer_name = name
            customer_email = customers[name]['email']
            
            # כתיבת תוכן המייל - מותאם אישית
            subject = f"שלום {customer_name}, עדכון חשוב מהעסק שלנו"
            body = f"""Dear {customer_name},

Thank you for registering on our website! 

Here are your account details:
• Username: {customer_name}
• Password: {customers[name]['password']}

If you have any questions, feel free to reply to this email.

The Support Team"""

            # יצירת מבנה המייל
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = customer_email

            # שליחת המייל
            server.sendmail(from_email, customer_email, msg.as_string())
            print(f"מייל נשלח בהצלחה אל: {customer_name} ({customer_email})")

# הפעלת הפונקציה
# send_customer_emails_from_json("aviv")
# user_scores = {"Alice": 95, "Bob": 88, "Charlie": 92}
# print(user_scores.items())