import os
from typing import List
from dotenv import load_dotenv, find_dotenv
from requests import Response, post

FAILED_LOAD_API_KEY = "Failed to load MailGun API key."
FAILED_LOAD_DOMAIN = "Failed to load MailGun domain."
ERROR_SENDING_EMAIL = "Error in sending confirmation email, user registration failed."

load_dotenv(find_dotenv())

class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    def send_email(
        email: List[str], subject: str, text: str
    ):
        MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", None)
        MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", None)

        FROM_TITLE = "Email Confirmation"
        FROM_EMAIL = f"do-not-reply@{MAILGUN_DOMAIN}"

        if MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)

        if MAILGUN_DOMAIN is None:
            raise MailGunException(FAILED_LOAD_DOMAIN)

        response = post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": email[0],
                "subject": subject,
                "text": text
            },
        )

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_EMAIL)

        return response
