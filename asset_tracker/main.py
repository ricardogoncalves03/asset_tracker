from data_fetcher import fetch_closing_prices
from email_sender import EmailSender


def main():
    tickers = ["VWCE.DE", "QDVE.DE", "VUAA.DE", "SXRV.DE"]
    current_closing_prices, previous_closing_prices = fetch_closing_prices(tickers)

    email_sender = EmailSender()
    email_message = email_sender.create_message(
        "Daily Closing Prices", current_closing_prices, previous_closing_prices
    )
    email_sender.send_message(email_message)


if __name__ == "__main__":
    main()
