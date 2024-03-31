

import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime

from flask import Flask, render_template, request, Response



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/captured'
app.config['AUDIO_FOLDER'] = 'static/audio'

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def perform_ocr_and_audio(image_path):
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def adjust_brightness_contrast(image, alpha=1.0, beta=0):
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted

    # Increase brightness and contrast of the image
    img_adjusted = adjust_brightness_contrast(img, alpha=1.5, beta=20)

    # Save the adjusted image
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    adjusted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'adjusted_image_{timestamp}.jpg')

    cv2.imwrite(adjusted_image_path, cv2.cvtColor(img_adjusted, cv2.COLOR_RGB2BGR))

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img_adjusted)

    # Print the extracted text
    print(text)

    # Convert the extracted text to speech
    tts = gTTS(text=text, lang='en')


    # Save the audio file
        
    audio_file = os.path.join(app.config['AUDIO_FOLDER'], f'output_{timestamp}.mp3')

    tts.save(audio_file)


    return text, audio_file, adjusted_image_path, timestamp


