

import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime



#timestamp = datetime.now().isoformat().replace("-", "").replace(":", "").replace(".", "")

# Construct the filename using the formatted timestamp
#filename = f"image_{timestamp}.jpg"

# Define the image path
image_path = r"C:\Users\Home\Downloads\image.jpg"

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


# Load the image
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(img)

 # Print the extracted text
print(text)

 