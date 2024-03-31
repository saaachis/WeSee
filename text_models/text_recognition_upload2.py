

import cv2
import pytesseract
from gtts import gTTS
import os
import io

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def perform_ocr_and_audio(image_path):

    # Load the image
    img = cv2.imread('img.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform OCR
    text = pytesseract.image_to_string(img)

    # Print the extracted text
    print(text)

    # Initialize gTTS
    tts = gTTS(text=text, lang='en')  # Specify language if needed

    audio_data = io.BytesIO()

    # Save the audio to the buffer in MP3 format (adjust format if desired)
    tts.write_to_fp(audio_data)

    # Seek to the beginning of the buffer to ensure correct reading
    audio_data.seek(0)

    return text, audio_data.getvalue()


