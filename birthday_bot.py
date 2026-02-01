import base64
import csv
import os
from datetime import date
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ['GMAIL_REFRESH_TOKEN'],
        client_id=os.environ['GMAIL_CLIENT_ID'],
        client_secret=os.environ['GMAIL_CLIENT_SECRET'],
        token_uri='https://oauth2.googleapis.com/token'
    )
    return build('gmail', 'v1', credentials=creds)


def send_email(service, to_email, name):
    msg = EmailMessage()
    msg['To'] = to_email
    msg['From'] = os.environ['SENDER_EMAIL']
    msg['Subject'] = f"🎉 Happy Birthday {name} 🎂"

    msg.set_content(f"""
Hi {name},

🎂 Happy Birthday!
Wishing you success, health, and happiness.

Best wishes,
Kirtan
""")

    encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={'raw': encoded_msg}
    ).execute()

def main():
    today = date.today().strftime("%m-%d")
    service = get_gmail_service()

    with open('birthdays.csv', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Normalize keys and values
            row = {k.strip().lower(): v.strip() for k, v in row.items()}

            if row['dob'][5:] == today:
                send_email(service, row['email'], row['name'])



if __name__ == "__main__":
    main()
