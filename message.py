import json
import smtplib
from email.mime.text import MIMEText

def send_customer_emails_from_json(name):
    from_email = "326406501@ziv-school.com" 
    password = "hmmn mwuh jpbg eahl"            

    with open('users.json', 'r', encoding='utf-8') as file:
        customers = json.load(file)  
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:          
            server.login(from_email, password)
            customer_name = name
            customer_email = customers[name]['email']
            
            subject = f"שלום {customer_name}, עדכון חשוב מהעסק שלנו"
            body = f"""Dear {customer_name},

Thank you for registering on our website! 

Here are your account details:
• Username: {customer_name}
• Password: {customers[name]['password']}

If you have any questions, feel free to reply to this email.

The Support Team"""

            
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = customer_email

          
            server.sendmail(from_email, customer_email, msg.as_string())
            print(f"מייל נשלח בהצלחה אל: {customer_name} ({customer_email})")

