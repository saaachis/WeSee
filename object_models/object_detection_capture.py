
from flask import Flask
import cv2
import torch
from gtts import gTTS
import os
from datetime import datetime
from PIL import Image
import numpy as np

app = Flask(__name__, static_folder='static')


app.config['AUDIO_FOLDER'] = 'static/audio'



def adjust_brightness_contrast(img, alpha=1.0, beta=0):

    # Apply brightness and contrast adjustment
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    return adjusted_img

  
def perform_object_detection():
    cap = cv2.VideoCapture(0)
    
    # Load a pre-trained model. Here, we're assuming YOLOv5; adjust as needed.
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)

    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            img_path = 'static/captured/captured_image.jpg'
            cv2.imwrite(img_path, frame)
            print("Image captured and saved.")

            adjusted_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=20)

            adjusted_img_path = 'static/captured/adjusted_captured_image.jpg'

            cv2.imwrite(adjusted_img_path, adjusted_frame)
            print("Adjusted Image captured and saved.")

            # Perform detection
            results = model(adjusted_frame)

                  
            # Get detected objects and generate description
            detected_objects = results.pandas().xyxy[0]['name'].unique()
            if detected_objects.size > 0:
                objects_list = ", ".join(detected_objects)
                description_text = f"The objects detected in the image are: {objects_list}."
            else:
                description_text = "No objects detected."
            # Print the description

            # Generate audio from the description text
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            audio_path = os.path.join('static/audio', f'description_{timestamp}.mp3')
            tts = gTTS(description_text, lang='en')
            tts.save(audio_path)
            print(f"Audio description saved at: {audio_path}")

            img_filename = os.path.basename(adjusted_img_path)
            audio_filename = os.path.basename(audio_path)

            cap.release()
            cv2.destroyAllWindows()
            break

        elif key == 27:  # Press 'Esc' to exit
            cap.release()
            cv2.destroyAllWindows()
            break
        
    return description_text, img_filename, audio_filename


