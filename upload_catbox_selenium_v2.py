import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip

if len(sys.argv) < 2:
    print("❌ Usage: python upload_catbox_selenium.py <image_path>")
    input("Press Enter to exit...")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.isfile(file_path):
    print("❌ File not found:", file_path)
    input("Press Enter to exit...")
    sys.exit(1)

print(f"📤 Uploading '{file_path}' to Catbox...")

# Set up Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # remove 'new' if headless crashes
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://catbox.moe/")
    wait = WebDriverWait(driver, 10)

    # Wait for upload input
    upload_input = wait.until(EC.presence_of_element_located((By.NAME, "fileToUpload")))
    upload_input.send_keys(os.path.abspath(file_path))

    # Wait for and click the submit button
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    submit_button.click()

    # Wait for result link
    result = wait.until(EC.presence_of_element_located((By.ID, "uploaded")))
    link = result.get_attribute("value")
    pyperclip.copy(link)

    print("✅ Uploaded! Link copied to clipboard:")
    print(link)
except Exception as e:
    print("❌ Error:", str(e))
finally:
    driver.quit()
    input("Press Enter to exit...")
