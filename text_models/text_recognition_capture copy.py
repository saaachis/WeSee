
import cv2
import pytesseract
from gtts import gTTS
import os

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def perform_text_capture():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the image
            cv2.imwrite('static/captured_image.jpg', frame)

            cap.release()
            cv2.destroyAllWindows()
            print("Image captured and saved as captured_image.jpg")
            break

        elif key == 27:  # Press 'Esc' to exit
            break

    img = cv2.imread('static/captured_image.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    text_output = pytesseract.image_to_string(img)
    print("Recognized text:")
    print(text_output)

    # Convert recognized text to speech using gTTS
    tts = gTTS(text=text_output, lang='en')
    tts.save("static/audio/output_audio.mp3")

    return text_output




