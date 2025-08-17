import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip

if len(sys.argv) < 2:
    print("❌ Please provide a file path to upload.")
    input("Press Enter to exit...")
    sys.exit(1)

file_path = sys.argv[1]
print(f"📤 Uploading '{file_path}' to Catbox...")

options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
# Headless disabled for debugging
# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://catbox.moe/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "fileToUpload")))
    upload_input = driver.find_element(By.NAME, "fileToUpload")
    upload_input.send_keys(file_path)

    submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_btn.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "uploaded")))
    uploaded_link = driver.find_element(By.ID, "uploaded").get_attribute("value")
    print(f"✅ Uploaded! Link: {uploaded_link}")
    pyperclip.copy(uploaded_link)
    print("📋 Link copied to clipboard.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    input("Press Enter to exit...")
    driver.quit()
