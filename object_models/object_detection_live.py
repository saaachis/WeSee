
import cv2
import torch
import pyttsx3
from transformers import pipeline
import time




def object_detection():
    # Initialize the components
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    text_generator = pipeline('text-generation', model='gpt2')
    tts_engine = pyttsx3.init()

    def generate_scene_description(objects):
        description = ' and '.join(objects) + ' are visible in the scene.'
        return description

    cap = cv2.VideoCapture(0)
    last_speech_time = time.time() - 6

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detected_objects = [model.names[int(x)] for x in results.xyxy[0][:, -1]]

        if detected_objects and (time.time() - last_speech_time) >= 6:
            last_speech_time = time.time()
            scene_description = generate_scene_description(detected_objects)
            print(scene_description)
            tts_engine.say(scene_description)
            tts_engine.runAndWait()

        cv2.imshow('press c to stop detection.', results.render()[0])

        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return  detected_objects



