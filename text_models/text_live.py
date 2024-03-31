
import cv2
import pytesseract

# Set the path to the Tesseract executable (change this based on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to perform text detection on each frame
def detect_text(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use OpenCV's thresholding to preprocess the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Use Tesseract to perform OCR on the preprocessed image
    text_boxes = pytesseract.image_to_boxes(thresh)
    
    # Draw bounding boxes around the detected text regions
    for box in text_boxes.splitlines():
        box = box.split()
        x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
        cv2.putText(frame, box[0], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    return frame

# Open the camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Detect text and draw bounding boxes
    processed_frame = detect_text(frame)
    
    # Display the frame
    cv2.imshow('Text Detection', processed_frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
