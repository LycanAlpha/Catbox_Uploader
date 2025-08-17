import requests
import sys
import os
import pyperclip

if len(sys.argv) < 2:
    print("❌ No file passed.")
    input("Press Enter to exit...")
    sys.exit(1)

file_path = sys.argv[1]

if not os.path.isfile(file_path):
    print("❌ File not found.")
    input("Press Enter to exit...")
    sys.exit(1)

# Build the multipart payload manually
with open(file_path, 'rb') as f:
    files = {
        'file': (os.path.basename(file_path), f, 'application/octet-stream')
    }
    data = {
        'reqtype': 'fileupload'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
    }

    response = requests.post("http://catbox.moe/user/api.php", data=data, files=files, headers=headers)

print(f"Status code: {response.status_code}")
print(f"Text: {response.text}")

if response.status_code == 200 and response.text.startswith("http"):
    pyperclip.copy(response.text.strip())
    print("\n✅ Uploaded! URL copied to clipboard.")
else:
    print("\n❌ Upload failed.")

input("Press Enter to exit...")
