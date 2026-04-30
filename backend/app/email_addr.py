import smtplib
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from work_wh_files import path_for_dotenv

def send_confirmation_code(user_email):

    code = str(random.randint(100000, 999999))
    
    load_dotenv(dotenv_path = path_for_dotenv()) 

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = "Код подтверждения"
    body = f"Ваш код для подтверждения: {code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        #print("Письмо отправлено!")
        return code 
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


