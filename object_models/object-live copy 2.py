
import cv2
import torch
import pyttsx3
from transformers import pipeline

# Initialize YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True) 

# Initialize Hugging Face pipeline for text generation (replace 'gpt2' with your chosen model)
text_generator = pipeline('text-generation', model='gpt2')

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def generate_scene_description(objects):
    # Placeholder function to generate a scene description from detected objects.
    # You might need to customize this part to integrate contextual scene understanding based on your project requirements.
    description = ' and '.join(objects) + ' are visible in the scene.'
    return description

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects in the frame
    results = model(frame)

    # Extract detected object names
    detected_objects = [model.names[int(x)] for x in results.xyxy[0][:, -1]]

    # Generate scene description based on detected objects
    if detected_objects:
        scene_description = generate_scene_description(detected_objects)
        print(scene_description)  # Optional: print the description

        # Use text generation model for more elaborate descriptions (optional)
        # generated_description = text_generator(scene_description, max_length=50, num_return_sequences=1)[0]['generated_text']
        # print(generated_description)  # Optional: print the generated description

        # Convert text description to speech
        tts_engine.say(scene_description)
        tts_engine.runAndWait()

    # Display the frame with detections
    cv2.imshow('YOLOv5 Object Detection', results.render()[0])

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break


cap.release()
cv2.destroyAllWindows()
