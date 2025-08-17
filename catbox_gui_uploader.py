# Save as catbox_gui_fixed.py or overwrite catbox_gui_uploader.py
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from threading import Thread
import requests
import pyperclip
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CatboxUploader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🐱 Catbox Uploader")
        self.geometry("400x350")
        self.resizable(False, False)

        # Load cat image
        try:
            image = Image.open("cat.png").resize((100, 100))
            self.cat_img = ctk.CTkImage(light_image=image, dark_image=image, size=(100, 100))
            self.cat_label = ctk.CTkLabel(self, image=self.cat_img, text="")
            self.cat_label.pack(pady=(10, 5))
        except:
            print("Cat image not found or invalid. Skipping image.")

        self.label = ctk.CTkLabel(self, text="Select a file to upload to Catbox", font=("Arial", 16), text_color="lime")
        self.label.pack(pady=5)

        self.upload_button = ctk.CTkButton(self, text="📂 Browse File", command=self.browse_file)
        self.upload_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Waiting...", font=("Arial", 14))
        self.status_label.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            Thread(target=self.upload_file, args=(file_path,)).start()

    def upload_file(self, file_path):
        self.status_label.configure(text="📤 Uploading...")
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    "https://catbox.moe/user/api.php",
                    data={"reqtype": "fileupload"},
                    files={"fileToUpload": f}
                )

            if response.status_code == 200 and response.text.startswith("https://"):
                pyperclip.copy(response.text)
                self.status_label.configure(text="✅ Uploaded! URL copied to clipboard")
            else:
                self.status_label.configure(text=f"❌ Upload failed: {response.text}")

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {e}")


if __name__ == "__main__":
    app = CatboxUploader()
    app.mainloop()
