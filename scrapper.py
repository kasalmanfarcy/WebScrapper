from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd

def sanitize_filename(name):
    
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'_+', '_', name)
    return name

count = 2500
page_count = 1
total_page = 388
skipPage = 251



service = Service('chromedriver-linux64/chromedriver')
chromeOptions = Options()
chromeOptions.add_argument("--start-maximized")

print("Initializing the Chrome WebDriver...")
driver = webdriver.Chrome(service=service, options=chromeOptions)

# Set to track clicked button IDs
clicked_buttons = set()

# Dictionary to store the count of how many times each button name has been used
button_click_count = {}

# Create a DataFrame to store scraped information
df = pd.DataFrame(columns=[
    'Call Type', 'Account', 'Recorded By', 'Recorded Date',
    'Duration', 'Score', 'Sentiment', 'Speakers', 'Summary'
])

try:
    # Login process
    print("Opening Traq.ai login page...")
    driver.get('https://app.traq.ai/login.aspx')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'txtUserName')))
    time.sleep(1)  # Wait a moment for the page to load

    print("Entering email address...")
    emailField = driver.find_element(By.ID, 'txtUserName')
    emailField.send_keys('Your Login Id')

    print("Entering password...")
    passwordField = driver.find_element(By.ID, 'txtPassword')
    passwordField.send_keys('Your Login Password')

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
                count += 1 # Initialize the counter for this button name

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

                # Scrape Call Overview Data
                print("Extracting Call Overview Data...")
                # Scrape Call Type
                call_type_element = driver.find_element(By.ID, 'CallAnalysisPanel_ddCallType')
                selected_option = call_type_element.find_element(By.XPATH, ".//option[@selected='selected']")
                call_type = selected_option.text.strip()

                # Scrape Account
                account_element = driver.find_element(By.ID, 'CallPreviewPanelAccountName')
                account = account_element.text.strip()

                # Scrape Recorded By
                recorded_by_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Recorded by:')]/following-sibling::div")
                recorded_by = recorded_by_element.text.strip()

                # Scrape Recorded Date
                recorded_date_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Recorded:')]/following-sibling::div//div[@class='mr-15']")
                recorded_date = recorded_date_element.text.strip()

                # Scrape Duration
                duration_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Duration:')]/parent::div")
                duration_text = duration_element.text.split("Duration:")[-1].strip()

                # Scrape Score
                score_element = driver.find_element(By.ID, 'CallAnalysisPanel_divCallScoreSm')
                score = score_element.text.strip()

                # Scrape Sentiment
                sentiment_element = driver.find_element(By.ID, 'CallAnalysisPanel_divSentimentScoreSm')
                sentiment = sentiment_element.text.strip()

                # Scrape Speakers
                speaker_elements = driver.find_elements(By.CSS_SELECTOR, 'div.speakerRow')
                speaker_names = [speaker.find_element(By.CSS_SELECTOR, 'input.speakerInputBox').get_attribute('value') for speaker in speaker_elements]
                speakers = ', '.join(speaker_names)  # Join speakers into a single string

                # Scrape Meeting Summary
                summary_element = driver.find_element(By.ID, 'analysisValue_short_summary')
                summary = summary_element.text.strip()

                # Create a new DataFrame for the current button's data

                # (Scraping process remains the same, as per your original code)

                # Create a new DataFrame for the current button's data
                temp_df = pd.DataFrame({
                    'Call Type': [call_type],
                    'Account': [account],
                    'Recorded By': [recorded_by],
                    'Recorded Date': [recorded_date],
                    'Duration': [duration_text],
                    'Score': [score],
                    'Sentiment': [sentiment],
                    'Speakers': [speakers],
                    'Summary': [summary]
                })

                # Concatenate the temporary DataFrame with the main DataFrame
                df = pd.concat([df, temp_df], ignore_index=True)

                # Save the DataFrame to Excel file after each scrape
                df.to_excel('scraped_data.xlsx', index=False)
                print(f"Data for {button_name} has been saved to 'scraped_data.xlsx'.")

                # Save transcription to a file using sequential numbering for button names
                transcription_text = ''
                transcription_blocks = driver.find_elements(By.CLASS_NAME, 'transcription-block-container')

                if transcription_blocks:
                    print(f"Found {len(transcription_blocks)} transcription blocks, processing them all...")

                    for block in transcription_blocks:
                        try:
                            speaker = block.find_element(By.CLASS_NAME, 'speaker-def').text.strip()
                            print(f"Speaker: {speaker}")

                            transcription_content = block.find_element(By.CSS_SELECTOR, 'p.transcription-block')

                            timestamp = block.find_element(By.CLASS_NAME, 'transcription-timestamp').text.strip()
                            
                            # Concatenating block transcription into the full text
                            block_transcription = f"Speaker: {speaker}\nTime: {timestamp}\nText: {transcription_content.text}\n\n"
                            transcription_text += block_transcription  # Concatenate to transcription text

                            print(f"Formatted Transcription Block:\n{block_transcription}")

                        except Exception as e:
                            print(f"An error occurred while processing a block: {e}") # Concatenate to transcription text

                    # Save the transcription with a sequentially numbered filename
                    if transcription_text:
                          # Increment the count for this button name
                        file_name = f"{count}_{sanitize_filename(button_name)}.txt"

                        print(f"Saving the transcription text to '{file_name}'...")
                        with open(file_name, 'w', encoding='utf-8') as file:
                            file.write(transcription_text)

                        print(f"Transcription has been saved successfully to '{file_name}'.")
                    else:
                        print("No transcription text was created to save.")
                else:
                    print("No transcription blocks were found on the page.")

                clicked_buttons.add(button_id)  # Track clicked button IDs

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
                clicked_buttons.clear()
                print("Clicking 'Next Page' to load the next table...")
                next_button.click()
                time.sleep(10)  # Wait for the next page to load
                
            else:
                print("No more pages available, exiting the loop.")
                break

finally:
    print("Closing the browser...")
    driver.quit()
