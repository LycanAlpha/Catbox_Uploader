import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import pyperclip
import os

def upload_to_catbox(file_path):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f}
            )
        if response.status_code == 200 and response.text.startswith("https://"):
            pyperclip.copy(response.text)
            return response.text
        else:
            raise Exception(f"Upload failed: {response.text}")
    except Exception as e:
        return f"❌ Error: {e}"

def on_drop(event=None):
    file_path = filedialog.askopenfilename()
    if file_path:
        status.set("📤 Uploading...")
        root.update_idletasks()
        result = upload_to_catbox(file_path)
        status.set(result)
        messagebox.showinfo("Upload Result", f"{result}")

# GUI setup
root = tk.Tk()
root.title("Catbox Drag & Drop Uploader")
root.geometry("400x180")
root.resizable(False, False)

label = tk.Label(
    root, text="📁 Drop a file here to upload to Catbox",
    font=("Segoe UI", 12), pady=20
)
label.pack()

button = tk.Button(root, text="📂 Select File", command=on_drop)
button.pack(pady=10)

status = tk.StringVar()
status.set("Ready.")
status_label = tk.Label(root, textvariable=status, fg="gray")
status_label.pack(pady=5)

root.mainloop()
