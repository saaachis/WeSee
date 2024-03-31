
import cv2
import torch

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to the RGB color space
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Make detections
    results = model(frame_rgb)

    # Extract data for drawing
    labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    
    # Draw rectangles and labels
    for label, cord in zip(labels, cord):
        x1, y1, x2, y2, conf = int(cord[0]*frame.shape[1]), int(cord[1]*frame.shape[0]), \
                               int(cord[2]*frame.shape[1]), int(cord[3]*frame.shape[0]), cord[4]
        label_name = model.names[int(label)]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0, 255), 2)

    # Display the resulting frame
    cv2.imshow('YOLOv5 Object Detection', frame)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
