# Image Steganography with Encryption

This project is a basic implementation of image steganography combined with encryption using the Python programming language. It allows users to hide a secret message inside an image file, and later extract and decrypt the message using a provided passcode.

## Features

- *Image Loading*: Load an image from your file system to embed a message.
- *Message Encryption*: Encrypt a message using the Fernet symmetric encryption.
- *Message Embedding*: Embed the encrypted message into the image using image pixel manipulation.
- *Message Extraction*: Extract and decrypt the message from the image using the same passcode.

## Requirements

- Python 3.x
- OpenCV
- Cryptography
- Tkinter
- Pillow

## Installation

Install the required libraries using pip:

```bash
pip install opencv-python cryptography Pillow
