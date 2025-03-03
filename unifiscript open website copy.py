from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pytz

# Define the login URL and the target URL
login_url = "https://unifi.dev.powerflex.io/manage/account/login?redirect=%2Fmanage"
target_url = "https://unifi.dev.powerflex.io/manage/4iaxxmxp/syslog/clients"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the WebDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the login URL
driver.get(login_url)

# Pause for 30 seconds to allow manual login
print("Please log in manually within 30 seconds...")
time.sleep(30)

tz = pytz.timezone('US/Pacific')
def extract_data():
    # Navigate to the target URL
    driver.get(target_url)

    # Wait for the target page to load completely
    time.sleep(30)  # Adjust the sleep time if needed

    # Extract the entire HTML content of the target page
    page_html = driver.page_source

    # Search for the specific string in the HTML content
    search_string = "POWERFLEX-DMZ"
    if search_string in page_html:
        print("Success: Found the string!")
        location = page_html.find(search_string)
        print(f"Location: {location}")

        # Locate the table containing the specific string
        try:
            table = driver.find_element(By.XPATH, f"//table[contains(., '{search_string}')]")
            print("Table found")

            # Extract the table HTML
            table_html = table.get_attribute('outerHTML')
            print("Table HTML:")
            print(table_html)

            # Parse the table HTML with BeautifulSoup
            soup = BeautifulSoup(table_html, 'html.parser')
            table = soup.find('table')

            # Function to convert 'Today at' to the actual date
            def convert_today_to_date(date_time_str):
                if 'Today at' in date_time_str:
                    # Get the current date
                    today_date = datetime.now().strftime('%b %d, %Y')
                    # Extract the time part from the string
                    time_part = date_time_str.split('Today at ')[1]
                    # Combine the current date with the time part
                    return f"{today_date} {time_part}"
                return date_time_str

            # Extract data into a list of dictionaries
            data = []
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    description = columns[0].get_text(strip=True)
                    date_time = columns[1].get_text(strip=True)
                    date_time = convert_today_to_date(date_time)
                    data.append({'Description': description, 'Date/Time': date_time})

            # Create a DataFrame from the data
            df = pd.DataFrame(data)
            now = datetime.now(tz=tz)
            now_str = now.strftime("%m-%d-%Y_%H-%M-%S")

            # Save the DataFrame to an Excel file
            filename = 'scarped_data_' + now_str + '.xlsx'
            df.to_excel(filename, index=False)
            print("Data saved to " + filename)

            # Print the DataFrame to the terminal
            print(df)
        except Exception as e:
            print(f"Error locating table: {e}")
    else:
        print("String not found.")

# Loop to extract data every 20 minutes
try:
    while True:
        extract_data()
        print("Waiting for 20 minutes before the next extraction...")
        time.sleep(1200)  # Wait for 20 minutes (1200 seconds)
except KeyboardInterrupt:
    print("Process interrupted by user.")

# Close the WebDriver
driver.quit()
