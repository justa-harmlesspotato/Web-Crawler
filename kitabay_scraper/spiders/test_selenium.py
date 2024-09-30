from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set Chrome options (you can customize these options as needed)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start browser maximized
chrome_options.add_argument("--disable-infobars")  # Disable infobars
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

# Initialize the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the target URL
    driver.get("https://kitabay.com/collections/fiction-mystery-crime-thriller")
    time.sleep(5)  # Wait for the page to load completely

    # Print the page title to confirm it's loaded
    print("Page Title:", driver.title)

    # Get the page source and print it (or do other actions as needed)
    page_source = driver.page_source
    print(page_source[:1000])  # Print the first 1000 characters of the page source

finally:
    # Close the browser
    driver.quit()
