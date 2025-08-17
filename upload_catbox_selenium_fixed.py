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
# options.add_argument("--headless=new")  # Uncomment if you want it hidden
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("🌐 Opening Catbox.moe...")
    driver.get("https://catbox.moe/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dropzoneUpload")))

    # Inject file input
    driver.execute_script("""
        let input = document.createElement('input');
        input.type = 'file';
        input.id = 'realFileInput';
        input.style.display = 'block';
        document.getElementById('dropzoneUpload').appendChild(input);
    """)
    time.sleep(1)

    # Upload file
    file_input = driver.find_element(By.ID, "realFileInput")
    file_input.send_keys(file_path)
    time.sleep(2)

    # Trigger upload
    driver.execute_script("Dropzone.instances[0].processQueue();")
    print("📡 Upload triggered...")

    # Wait for the uploaded link to appear
    print("⌛ Waiting for upload to complete...")
    result_link = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dz-success .dz-details a"))
    ).get_attribute("href")

    print(f"✅ Uploaded! Link: {result_link}")

except Exception as e:
    print("❌ Error occurred:")
    print(e)

finally:
    input("Press Enter to exit...")
    driver.quit()
