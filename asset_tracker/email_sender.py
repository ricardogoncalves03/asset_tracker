import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config


class EmailSender:
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.service = self.get_gmail_service()

    def get_gmail_service(self):
        """
        Authenticates and returns the Gmail service instance.

        Returns:
            service: The Gmail API service instance.
        """
        creds = None
        token_path = os.path.join(self.base_dir, "token.json")
        credentials_path = os.path.join(self.base_dir, "credentials.json")
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        service = build("gmail", "v1", credentials=creds)
        return service

    def create_message(
        self,
        subject: str,
        closing_prices: dict[str, float],
        first_closing_prices: dict[str, float],
    ):
        """
        Creates an email message.

        Args:
            subject (str): The subject of the email.
            closing_prices (Dict[str, float]): The latest closing prices.
            first_closing_prices (Dict[str, float]): The first closing prices.

        Returns:
            dict: The email message in raw format.
        """
        message = MIMEMultipart("alternative")
        message["to"] = ", ".join(Config.RECIPIENT_EMAILS)
        message["from"] = Config.SENDER_EMAIL
        message["subject"] = subject

        # Create the plain-text part
        plain_text = f"{subject}\nTicker\tPrice\t% Change\n"
        for ticker, price in closing_prices.items():
            first_price = first_closing_prices.get(ticker, price)
            pct_change = (
                (price - first_price) / first_price
            ) * 100 
            plain_text += f"{ticker.split('.')[0]}\t{price:.2f}\t{pct_change:.2f}%\n"

        part1 = MIMEText(plain_text, "plain")

        # Generate the table rows for the HTML part
        table_rows = ""
        for ticker, price in closing_prices.items():
            first_price = first_closing_prices.get(ticker, price)
            pct_change = (
                ((price - first_price) / first_price) * 100 if first_price != 0 else 0
            )
            table_rows += f"<tr><td>{ticker.split('.')[0]}</td><td>{price:.2f}</td><td>{pct_change:.2f}%</td></tr>"

        # Read and format the HTML template
        email_template_path = os.path.join(
            self.base_dir, "asset_tracker", "email_template.html"
        )
        with open(email_template_path, "r") as file:
            html_template = file.read()
        html_content = html_template.replace("{{table_rows}}", table_rows)
        html_content = html_content.replace("{{report_title}}", subject)

        part2 = MIMEText(html_content, "html")

        # Attach parts into message container.
        message.attach(part1)
        message.attach(part2)
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {"raw": raw}

    def send_message(self, message: dict):
        """
        Sends an email message.

        Args:
            message (dict): The email message in raw format.

        Returns:
            dict: The sent message details.
        """
        try:
            message = (
                self.service.users()
                .messages()
                .send(userId="me", body=message)
                .execute()
            )
            print("Message Id: %s" % message["id"])
            return message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
