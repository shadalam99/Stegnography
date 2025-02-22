import cv2
import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Function to generate a key from password
def generate_key(password):
    return Fernet.generate_key()

# Encrypt the message using Fernet
def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

# Decrypt the message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

# Function to embed the encrypted message into the image
def embed_message():
    global img, encrypted_msg, key
    msg = message_entry.get()
    password = password_entry.get()
    
    if not msg or not password:
        messagebox.showerror("Error", "Please enter both message and password.")
        return
    
    key = generate_key(password.encode())
    encrypted_msg = encrypt_message(msg, key)
    
    n, m, z = 0, 0, 0
    for byte in encrypted_msg:
        img[n, m, z] = byte
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3
    
    cv2.imwrite("encryptedImage.jpg", img)
    messagebox.showinfo("Success", "Message embedded and image saved as 'encryptedImage.jpg'.")
    os.system("start encryptedImage.jpg")

# Function to extract and decrypt the message from the image
def extract_message():
    global img, encrypted_msg, key
    pas = decrypt_password_entry.get()
    
    if password_entry.get() != pas:
        messagebox.showerror("Error", "Unauthorized access. Wrong passcode.")
        return
    
    n, m, z = 0, 0, 0
    extracted_bytes = bytearray()
    
    for _ in range(len(encrypted_msg)):
        extracted_bytes.append(img[n, m, z])
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3
    
    try:
        decrypted_msg = decrypt_message(bytes(extracted_bytes), key)
        messagebox.showinfo("Decrypted Message", f"Decrypted Message: {decrypted_msg}")
    except Exception as e:
        messagebox.showerror("Error", "Failed to decrypt. Possible wrong passcode or corrupted data.")

# Function to load the image
def load_image():
    global img
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Image not found or unsupported format.")
            return
        img_label.config(text=f"Loaded Image: {os.path.basename(file_path)}")
        messagebox.showinfo("Success", "Image loaded successfully.")

# Initialize the main window
root = tk.Tk()
root.title("Image Steganography with Encryption")
root.geometry("600x500")
root.configure(bg="#2E3440")  # Dark background color

# Custom Fonts
title_font = ("Helvetica", 20, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")

# Colors
bg_color = "#2E3440"  # Dark background
fg_color = "#D8DEE9"  # Light text color
button_color = "#5E81AC"  # Blue button color
entry_color = "#4C566A"  # Darker background for entry widgets

# Title Label
title_label = tk.Label(root, text="Image Steganography with Encryption", font=title_font, bg=bg_color, fg=fg_color)
title_label.pack(pady=20)

# Load Image Button
load_image_button = tk.Button(root, text="Load Image", command=load_image, font=button_font, bg=button_color, fg=fg_color)
load_image_button.pack(pady=10)

# Label to show loaded image
img_label = tk.Label(root, text="No image loaded", font=label_font, bg=bg_color, fg=fg_color)
img_label.pack(pady=5)

# Message Entry
message_label = tk.Label(root, text="Enter Secret Message:", font=label_font, bg=bg_color, fg=fg_color)
message_label.pack(pady=5)
message_entry = tk.Entry(root, width=50, font=label_font, bg=entry_color, fg=fg_color)
message_entry.pack(pady=5)

# Password Entry
password_label = tk.Label(root, text="Enter Passcode:", font=label_font, bg=bg_color, fg=fg_color)
password_label.pack(pady=5)
password_entry = tk.Entry(root, width=50, show="*", font=label_font, bg=entry_color, fg=fg_color)
password_entry.pack(pady=5)

# Embed Message Button
embed_button = tk.Button(root, text="Embed Message", command=embed_message, font=button_font, bg=button_color, fg=fg_color)
embed_button.pack(pady=10)

# Decrypt Password Entry
decrypt_password_label = tk.Label(root, text="Enter Passcode for Decryption:", font=label_font, bg=bg_color, fg=fg_color)
decrypt_password_label.pack(pady=5)
decrypt_password_entry = tk.Entry(root, width=50, show="*", font=label_font, bg=entry_color, fg=fg_color)
decrypt_password_entry.pack(pady=5)

# Extract Message Button
extract_button = tk.Button(root, text="Extract Message", command=extract_message, font=button_font, bg=button_color, fg=fg_color)
extract_button.pack(pady=10)

# Run the application
root.mainloop()