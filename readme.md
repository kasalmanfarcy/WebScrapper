# Traq.ai Web Scraping Scripts

This repository contains two Python scripts, `scrapper.py` and `audioscrapper.py`, designed to automate data extraction from the Traq.ai platform. Both scripts use Selenium to log into Traq.ai, navigate through call records, and save extracted data locally.

## Scripts Overview

### scrapper.py

`scrapper.py` automates the extraction of call data from Traq.ai, such as call type, account, recorded date, duration, score, sentiment, participants, and transcription data. The script saves this information to an Excel file and transcription files.

**Functionality:**
1. Logs into Traq.ai.
2. Navigates to the main dashboard and selects "All" from a dropdown to access all call records.
3. Iterates through each call record, scrapes call information and transcription data, and saves the data in:
   - An Excel file containing call information.
   - Text files containing call transcriptions.

**Output:**
- `calls_data.xlsx`: Excel file with call information.
- Individual `.txt` files for each call transcription.

### audioscrapper.py

`audioscrapper.py` automates the download of audio/video files from each call record on Traq.ai.

**Functionality:**
1. Logs into Traq.ai.
2. Bypasses pop-ups and navigates to the main dashboard.
3. Iterates through each call record, accesses the audio/video file, and downloads it as an `.mp4` file.
4. Loops through multiple pages to download files for all call records up to a set page limit.

**Output:**
- Audio files saved locally in the format `[ID]_[button_name]_audio.mp4`.

## Setup

### Prerequisites

- Python 3.8 or later
- Chrome WebDriver (compatible with your version of Chrome)
- Libraries listed in `requirements.txt`

### Install Requirements

To install the necessary libraries, run:
```bash
pip install -r requirements.txt
```

### Configuration

- **Login Credentials:** Update the email and password fields in both scripts with your Traq.ai login credentials.
- **WebDriver Path:** Place `chromedriver` in an accessible directory, and update the path if necessary.

## Usage

### Running scrapper.py

Execute `scrapper.py` with:
```bash
python scrapper.py
```

This script will log into Traq.ai, scrape call data and transcription blocks, and save them into Excel and text files.

### Running audioscrapper.py

Execute `audioscrapper.py` with:
```bash
python audioscrapper.py
```

This script will log into Traq.ai, navigate through call records, and download audio/video files up to a set page limit.

### Customizing Start Page

To begin from a specific page in either script, modify the `skipPage` variable:
```python
skipPage = 251  # Example start page
```



