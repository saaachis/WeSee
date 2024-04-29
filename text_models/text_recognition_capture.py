
import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    # Apply brightness and contrast adjustment
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted_img

def perform_text_capture():
    cap = cv2.VideoCapture(0)

    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the original image
            cv2.imwrite('static/captured/original_image.jpg', frame)

            # Adjust brightness and contrast
            adjusted_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=20)
            cv2.imwrite('static/captured/adjusted_image.jpg', adjusted_frame)

            cap.release()
            cv2.destroyAllWindows()
            print("Images captured and saved")

            break

        elif key == 27:  # Press 'Esc' to exit
            break

    img_path = 'static/captured/adjusted_image.jpg'
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        text_output = pytesseract.image_to_string(img)
        print("Recognized text:")
        print(text_output)

        if text_output.strip():  # Check if the recognized text is not empty

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Convert recognized text to speech using gTTS
            tts = gTTS(text=text_output, lang='en')
            audio_path = f"static/audio/output_audio_{timestamp}.mp3"
            tts.save(audio_path)

            return text_output, img_path, audio_path, timestamp
        else:
            return "Error: No text detected in the captured image", "", ""
    else:
        return "Error: Adjusted image not found", "", ""



