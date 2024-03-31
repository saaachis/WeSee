
from flask import Flask
import cv2
import torch
from gtts import gTTS
import os
from datetime import datetime
from PIL import Image

app = Flask(__name__, static_folder='static')


app.config['AUDIO_FOLDER'] = 'static/audio'


  # Use 0 for the default camera


def capture_objects(image_path):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    img = Image.open(image_path)
    results = model(img)
    detected_objects = results.pandas().xyxy[0]['name'].unique()

    if detected_objects.size > 0:
        objects_list = ", ".join(detected_objects)
        description_text = f"The objects detected in the image are: {objects_list}."
    else:
        description_text = "No objects detected."

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    tts = gTTS(description_text, lang='en')

    audio_path = os.path.join(app.config['AUDIO_FOLDER'], f'described_{timestamp}.mp3')
    tts.save(audio_path)
    
    return description_text, audio_path, timestamp
