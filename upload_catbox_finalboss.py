from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

file_path = sys.argv[1]
print(f"📤 Uploading '{file_path}' to Catbox...")

options = Options()
# options.add_argument("--headless=new")  # optional
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("🌐 Opening Catbox.moe...")
    driver.get("https://catbox.moe/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dropzoneUpload")))

    # Inject real file input
    driver.execute_script("""
        let input = document.createElement('input');
        input.type = 'file';
        input.id = 'realFileInput';
        input.style.display = 'block';
        document.getElementById('dropzoneUpload').appendChild(input);
    """)
    time.sleep(1)

    # Select file
    file_input = driver.find_element(By.ID, "realFileInput")
    file_input.send_keys(file_path)
    print("📁 File selected...")

    # Wait for file preview (Dropzone detects file)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dz-preview"))
    )
    print("📄 File queued, clicking upload...")

    upload_button = driver.find_element(By.ID, "uploadbutton")
    upload_button.click()

    print("⏳ Waiting for upload result...")

    result = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dz-success-mark ~ a"))
    )
    print(f"✅ Uploaded! Link: {result.get_attribute('href')}")

except Exception as e:
    print("❌ Error occurred:")
    print(e)

finally:
    driver.quit()
