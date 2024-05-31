import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SENDER_EMAIL: str = os.getenv('SENDER_EMAIL', '')
    RECIPIENT_EMAILS: list[str] = os.getenv('RECIPIENT_EMAILS', '').split(',')

    @staticmethod
    def validate():
        if not Config.SENDER_EMAIL:
            raise ValueError("SENDER_EMAIL environment variable is missing or empty")
        if not Config.RECIPIENT_EMAILS or any(email == '' for email in Config.RECIPIENT_EMAILS):
            raise ValueError("RECIPIENT_EMAILS environment variable is missing or empty")

# Validate configuration
Config.validate()
