
import cv2
import pytesseract
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Load the image
img = cv2.imread('/text_models/img.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Perform OCR
text = pytesseract.image_to_string(img)

# Print the extracted text
print(text)

# Initialize pyttsx3
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech

# Convert text to speech
engine.say(text)

# Play the speech
engine.runAndWait()



