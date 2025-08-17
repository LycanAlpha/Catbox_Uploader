import sys
import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) < 2:
    print("❌ No file path provided.")
    input("Press Enter to exit...")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.exists(file_path):
    print("❌ File not found:", file_path)
    input("Press Enter to exit...")
    sys.exit(1)

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-popup-blocking")
# Uncomment to run headless:
# chrome_options.add_argument("--headless=new")

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://catbox.moe/")
import time
time.sleep(5)  # wait for the page to actually load


try:
    upload_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "file"))
    )
    upload_input.send_keys(file_path)

    submit_button = driver.find_element(By.XPATH, '//input[@value="Upload"]')
    submit_button.click()

    # Wait for the link to appear
    link_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "url"))
    )

    url = link_field.get_attribute("value")
    if url.startswith("https://"):
        pyperclip.copy(url)
        print("✅ Uploaded! URL copied to clipboard:")
        print(url)
    else:
        print("❌ Upload failed. No URL returned.")
except Exception as e:
    print("❌ Error:", e)
finally:
    input("Press Enter to exit...")
    driver.quit()
