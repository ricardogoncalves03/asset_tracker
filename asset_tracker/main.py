from data_fetcher import fetch_closing_prices
from email_sender import EmailSender
from datetime import datetime, timedelta


def get_report_type() -> str:
    """
    Determines the type of report to generate based on the current date.

    Returns:
        str: The report type ('daily', 'weekly', 'monthly').
    """
    today = datetime.today()
    if today.weekday() in [5, 6]:  # Saturday or Sunday
        friday = today - timedelta(days=(today.weekday() - 4))
        return "weekly" if friday.month == today.month else "monthly"
    if today.weekday() == 4:  # Friday
        next_day = today + timedelta(days=1)
        if next_day.month != today.month:
            return "monthly"
        return "weekly"
    return "daily"


def main():
    """
    Main function to fetch closing prices, create and send the email report.
    """
    tickers = ["VWCE.DE", "QDVE.DE", "VUAA.DE", "SXRV.DE"]
    report_type = get_report_type()

    if report_type == "daily":
        subject = "Daily Closing Prices"
    elif report_type == "weekly":
        subject = "Weekly Closing Prices"
    elif report_type == "monthly":
        subject = "Monthly Closing Prices"

    current_closing_prices, first_closing_prices = fetch_closing_prices(
        tickers, report_type
    )

    email_sender = EmailSender()
    email_message = email_sender.create_message(
        subject, current_closing_prices, first_closing_prices
    )
    email_sender.send_message(email_message)


if __name__ == "__main__":
    main()
