
import cv2
import pytesseract
from gtts import gTTS
import os

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Load the image
img = cv2.imread('img.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Perform OCR
text = pytesseract.image_to_string(img)

# Print the extracted text
print(text)

# Initialize gTTS
tts = gTTS(text=text, lang='en')  # Specify language if needed

# Save the audio as MP3
tts.save('output.mp3')

# Play the audio using an external player (optional)

os.system("start output.mp3")  # Windows example