import cv2
import pytesseract
import numpy as np
import pyttsx3
import time


# Point pytesseract to where the tesseract executable is located
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



def perform_live_text():

    engine = pyttsx3.init()

    def detect_text(frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use OpenCV's thresholding to preprocess the image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Use Tesseract to perform OCR on the preprocessed image
        text = pytesseract.image_to_string(thresh)
        
        return text

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Variable to track the time of the last speech output
    last_speech_time = 0
    # Minimum gap between speeches in seconds
    speech_gap = 2

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Detect text in the frame
        detected_text = detect_text(frame)
    
        
        # Draw bounding boxes around the detected text
        h, w, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (w, 30), (0, 0, 0), -1)
        cv2.putText(frame, detected_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Get the current time
        current_time = time.time()
        
        # Check if 4 seconds have passed since the last speech output
        if detected_text and (current_time - last_speech_time) > speech_gap:
            # Speak the detected text
            engine.say(detected_text)
            engine.runAndWait()
            
            # Update the last speech time
            last_speech_time = current_time
        
        # Display the frame
        cv2.imshow('press c to stop detection.', frame)
        

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()



    


