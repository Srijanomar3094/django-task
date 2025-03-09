import smtplib
import json
import os
from dotenv import load_dotenv
import json

def send_email(event, context):
    try:
        data = json.loads(event["body"])
        receiver_email = data["receiver_email"]
        subject = data["subject"]
        body_text = data["body_text"]
        
        if not receiver_email or not subject or not body_text:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing required fields"})}


        sender_email = os.getenv("SENDER_EMAIL")
        password = os.getenv("SENDER_PASSWORD")

        message = f"Subject: {subject}\n\n{body_text}"
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

