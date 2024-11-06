# Traq.ai Data Scraper

This repository contains two Python scripts, `scrapper.py` and `audioscrapper.py`, designed to automate the extraction of call data and audio/video files from Traq.ai. The scripts leverage Selenium for browser automation and allow users to scrape various call-related details for data analysis and record-keeping.

## Prerequisites

1. **Python 3.x**: Ensure you have Python 3 installed on your machine.
2. **Google Chrome**: The scripts use Chrome for automation, so having the browser installed is required.
3. **ChromeDriver**: Download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) version for your Chrome browser and operating system.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kasalmanfarcy/WebScrapper
    cd your-repository-name
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Place `chromedriver` in the `chromedriver-linux64` folder (or update the path in the script if it is different).

## Scripts Overview

### 1. `scrapper.py`

This script logs into Traq.ai, navigates through call data pages, and scrapes various call details. The data is saved to both an Excel file and text transcription files.

- **Main Features**:
  - Login automation and session management.
  - Iterative row processing in tables with pagination support.
  - Data extraction including call type, account name, recorded date, duration, sentiment, and speakers.
  - Output: call data saved in an Excel file and transcription text files for each call.

- **Usage**:
  ```bash
  python scrapper.py
