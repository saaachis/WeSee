
import torch
from PIL import Image
from gtts import gTTS
import os

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load an image
img_path = r'C:\Users\Home\Downloads\one.png' # Update this to the path of your image
img = Image.open(img_path)

# Inference
results = model(img)

 # Get unique detected object names

detected_objects = results.pandas().xyxy[0]

# Generate a description of detected objects
description = []
for index, row in detected_objects.iterrows():
    description.append(f"{row['name']} with confidence {row['confidence']:.2f}")


description_text = ", ".join(description)
if not description:
    description_text = "No objects detected."

# Print the description
print(f"Detected objects: {description_text}")

# Text-to-Speech conversion
tts = gTTS(description_text, lang='en')
audio_save_path = 'C:\\Users\\Home\\Downloads\\output.mp3' # Update this to your desired path
tts.save(audio_save_path)

# Access the rendered image with detections (PIL image)
rendered_img = results.render()[0]  # results.render() returns a list of images
detected_img = Image.fromarray(rendered_img)

# Specify your desired save path for image
image_save_path = 'C:\\Users\\Home\\Downloads\\output.jpg'  # Update this to your desired path
detected_img.save(image_save_path)

print(f"Saved detected image to {image_save_path}")
print(f"Saved audio description to {audio_save_path}")
