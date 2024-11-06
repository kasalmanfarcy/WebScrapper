from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import requests

def sanitize_filename(name):
    
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'_+', '_', name)
    return name


count = 2500
page_count = 1
total_page = 388
skipPage = 251


# Setup for Chrome WebDriver
service = Service('chromedriver-linux64/chromedriver')
chromeOptions = Options()
chromeOptions.add_argument("--start-maximized")


print("Initializing the Chrome WebDriver...")
driver = webdriver.Chrome(service=service, options=chromeOptions)

# Set to track clicked button IDs
clicked_buttons = set()

# Dictionary to store the count of how many times each button name has been used
button_click_count = {}

def download_audio_file(audio_url, file_name):
    try:
        print(f"Downloading audio from {audio_url}...")
        response = requests.get(audio_url)
        response.raise_for_status()  # Check if the request was successful
        with open(file_name, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"Audio file saved as {file_name}")
        
    except Exception as e:
        print(f"An error occurred while downloading the audio: {e}")
try:
    # Login process
    print("Opening Traq.ai login page...")
    driver.get('https://app.traq.ai/login.aspx')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'txtUserName')))
    time.sleep(1)  # Wait for the page to load

    print("Entering email address...")
    emailField = driver.find_element(By.ID, 'txtUserName')
    emailField.send_keys('Your emailId')

    print("Entering password...")
    passwordField = driver.find_element(By.ID, 'txtPassword')
    passwordField.send_keys('Your Password')

    print("Submitting login form...")
    submitButton = driver.find_element(By.ID, 'btnSubmit')
    submitButton.click()

    WebDriverWait(driver, 10).until(EC.url_to_be('https://app.traq.ai/setup/'))
    print("Login successful, navigating to setup page...")

    driver.get('https://app.traq.ai/setup/')
    time.sleep(3)

    # Handling the 'Remind Me Later' popup
    print("Clicking 'Remind Me Later' button...")
    remindMeButton = driver.find_element(By.CSS_SELECTOR, 'a[data-target="#SnoozeOnboarding"]')
    remindMeButton.click()

    time.sleep(2)
    popupRemindMeButton = driver.find_element(By.CSS_SELECTOR, 'a.btn.mb-10.mt-5')
    popupRemindMeButton.click()

    time.sleep(5)
    print("Remind Me Later popup handled, navigating to main dashboard...")

    driver.get('https://app.traq.ai/')
    time.sleep(3)

    # Selecting 'All' from the dropdown menu
    print("Clicking dropdown menu to select 'All'...")
    dropdownMenu = driver.find_element(By.ID, 'gridMenu_RangeName')
    dropdownMenu.click()

    time.sleep(2)

    print("Clicking 'All' option in the dropdown...")
    allButton = driver.find_element(By.XPATH, "//div[text()='All' and @class='rangeFilterItem link-333 mb-10']")
    allButton.click()

    print("Dropdown 'All' option clicked successfully")
    time.sleep(5)

    # Function to check if the "Next Page" button is available and enabled
    def next_page_available():
        try:
            next_button = driver.find_element(By.XPATH, "//button[@title='Next Page' and not(@disabled)]")
            return next_button
        except Exception as e:
            return None
        
    while page_count < skipPage:
        next_button = next_page_available()
        if next_button:
            print(f"Moving to page {page_count + 1} by clicking 'Next Page' button...")
            next_button.click()
            time.sleep(10) 
            page_count += 1
        else:
            print("Unable to navigate to the 11th page. Exiting.")
            driver.quit()
            exit()

    # Loop through buttons and scrape transcription data
    while page_count <= total_page:
        button_found = False
        buttons = driver.find_elements(By.CSS_SELECTOR, "a[id^='ctl00_phBody_rgDashboard_ctl00_ctl']")

        for button in buttons:
            button_id = button.get_attribute("id")

            if button_id in clicked_buttons:  # Check if this button has already been clicked
                continue

            button_name = button.text.strip().replace(' ', '_')  # Extract the button name and sanitize it for file naming
            if button_name not in button_click_count:
                count += 1  # Initialize the counter for this button name

            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))

                print(f"Clicking the button with ID: {button_id} and name: {button_name}...")
                button.click()

                print(f"Button with ID: {button_id} clicked successfully")

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe.threadeditcontainer_currenteditor')))
                print("Page loaded after button click, locating transcription blocks...")

                # Switch to iframe to get transcription content
                print("Switching to the transcription iframe...")
                iframefb = driver.find_element(By.CSS_SELECTOR, 'iframe.threadeditcontainer_currenteditor')
                driver.switch_to.frame(iframefb)

                # Scraping audio URL from the iframe
                print("Scraping audio/video URL from the iframe...")

                # Click the play button
                print("Clicking the play button...")
                play_button = driver.find_element(By.CSS_SELECTOR, ".playBtnContainer")
                play_button.click()
                time.sleep(10)

                # Wait for the video element to appear and extract the audio URL
                print("Waiting for video element to load...")
                video_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#jp_video_0"))
                )

                # Get the audio URL from the video element
                audio_url = video_element.get_attribute("src")

                if audio_url:
                    audio_file_name = f"{count}_{button_name}_audio.mp4"
                      # Save as mp4 as it is a video URL
                    download_audio_file(audio_url, audio_file_name)

                # Optionally wait for some time to allow the audio to play if needed
                time.sleep(2)

                clicked_buttons.add(button_id) 
                time.sleep(5) # Track clicked button IDs

                # Use the 'Back' button to return to the table
                print("Clicking the 'Back' button to return to the table...")
                back_button = driver.find_element(By.CSS_SELECTOR, "div.circle-btn-link.mr-10.ml-5")
                back_button.click()

                # Switch back to default content (outside of iframe)
                driver.switch_to.default_content()

                button_found = True
                break

            except Exception as e:
                print(f"An error occurred while processing button with ID {button_id}: {e}")

        if not button_found:
            print("No more buttons to click on this page.")

            # Check if the 'Next Page' button is available
            next_button = next_page_available()
            if next_button:
                clicked_buttons.clear()  # Reset the clicked buttons for the new page
                print("Clicking 'Next Page' to load the next table...")
                next_button.click()
                time.sleep(10)  # Wait for the next page to load
                
            else:
                print("No more pages available, exiting the loop.")
                break

finally:
    print("Closing the browser...")
    driver.quit()
