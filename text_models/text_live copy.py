
import cv2
import pytesseract
import numpy as np


# Point pytesseract to where the tesseract executable is located
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


# Function to perform text detection on each frame
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

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Detect text in the frame
    detected_text = detect_text(frame)
    
    # Draw bounding boxes around the detected text
    h, w, _ = frame.shape
    cv2.rectangle(frame, (0, 0), (w, 50), (0, 0, 0), -1)
    cv2.putText(frame, detected_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Display the frame
    cv2.imshow('Text Detection', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

