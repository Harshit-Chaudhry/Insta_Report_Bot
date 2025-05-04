# Instagram Pakistani Account Reporter Bot

## Description

This Python project automates the process of finding and reporting Instagram accounts associated with specific hashtags that are identified as being based in Pakistan.

It uses Selenium and undetected-chromedriver for web scraping and browser automation.

## Features

*   Scrapes usernames from Instagram posts based on a predefined list of hashtags.
*   Filters scraped usernames to identify accounts located in Pakistan by checking the "About This Account" section.
*   Automatically reports the identified Pakistani accounts.
*   Saves the list of reported Pakistani usernames to a file (`pakistani_usernames.txt`).

## Prerequisites

*   Python 3.x installed.
*   Google Chrome browser installed.
*   Appropriate ChromeDriver version (managed by `webdriver-manager`).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd Insta_Report_Bot
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the script, you need to update the Instagram credentials in the `main.py` file:

```python
# main.py
credentials = InstagramCredentials(
    username="YOUR_INSTAGRAM_USERNAME", # Replace with your username
    password="YOUR_INSTAGRAM_PASSWORD"  # Replace with your password
)
```

You might also want to adjust the hashtags and other scraping parameters within `scraper1.py` or `main.py` as needed.

## Usage

Run the main script from the project's root directory:

```bash
python main.py
```

The script will perform the scraping, filtering, and reporting steps, printing progress to the console and saving the reported usernames to `pakistani_usernames.txt`.

## Dependencies

The project relies on the following Python packages:

*   pandas
*   ipykernel
*   numpy
*   selenium
*   beautifulsoup4
*   webdriver-manager
*   requests
*   undetected-chromedriver

These can be installed using the `requirements.txt` file as shown in the Installation section.

## Disclaimer

This tool automates actions on Instagram. Use it responsibly and ethically. Excessive or inappropriate use may violate Instagram's terms of service and could lead to account restrictions or suspension. The developers are not responsible for any misuse of this tool or consequences resulting from its use.