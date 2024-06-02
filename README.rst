# Asset Tracker

Asset Tracker is a Python-based tool designed to automate the process of tracking and analyzing the closing prices of specified assets, such as ETFs or Stocks. 
The tool can be configured to send daily, weekly, or monthly email reports with the latest closing prices and percentage changes.

## Features

- Fetches closing prices of specified assets using the `yfinance` library.
- Sends automated email reports using the Gmail API.
- Configurable to send daily, weekly, or monthly reports.
- Scheduled to run at 18:00 Lisbon time on weekdays.

## Setup Instructions

### Prerequisites

- Python 3.10
- Poetry (for dependency management)
- A Google account with access to the Gmail API

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/asset_tracker.git
    cd asset_tracker
    ```

2. **Install dependencies**:
    ```sh
    poetry install
    ```

3. **Set up Google API credentials**:
    - Follow the instructions to set up a project on the [Google Cloud Console](https://console.cloud.google.com/).
    - Enable the Gmail API and download the `credentials.json` file.
    - Place the `credentials.json` file in the root directory of the project.

4. **Set up the virtual environment**:
    ```sh
    source $(poetry env info --path)/bin/activate
    ```

5. **Run the main script**:
    ```sh
    python asset_tracker/main.py
    ```

## Usage

### Scheduling the Script

To schedule the script to run daily at 18:00 Lisbon time on weekdays, you can set up a cron job:

1. **Ensure the script is executable**:
    ```sh
    chmod +x run_script.sh
    ```

2. **Edit your crontab**:
    ```sh
    crontab -e
    ```

3. **Add the following line to schedule the script**:
    ```sh
    TZ='Europe/Lisbon'
    0 18 * * 1-5 /home/ricardo/Documents/dev/asset_tracker/run_script.sh >> /home/ricardo/Documents/dev/logs/cron_output.log 2>&1
    ```

### Environment Variables

Ensure the following environment variables are set:

- `PYTHONPATH` (optional): Points to the project directory.

### Email Configuration

The `email_sender.py` script is configured to use the Gmail API. Ensure you have valid credentials and tokens.

## Acknowledgements

- [yfinance](https://github.com/ranaroussi/yfinance) for fetching financial data.
- [Google API Python Client](https://github.com/googleapis/google-api-python-client) for Gmail API integration.
