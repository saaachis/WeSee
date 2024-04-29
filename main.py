

from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import cv2
import pytesseract
from gtts import gTTS
import threading

from text_models import text_recognition_upload
from text_models import text_recognition_capture
from text_models import text_recognition_live

from object_models import object_detection_upload
from object_models import object_detection_capture
from object_models import object_detection_live


app = Flask(__name__, static_folder='static')


app.config['UPLOAD_FOLDER'] = 'static/captured'
app.config['AUDIO_FOLDER'] = 'static/audio'


camera = cv2.VideoCapture(0)


@app.route('/')
def home():
    return render_template('home-page.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/text')
def text():
    return render_template('text-recognition.html')


@app.route('/text1')
def text1():
    return render_template('text-recognition-upload.html')


@app.route('/text-recognition', methods=['POST'])
def text_recognition():
    # Retrieve image data from the request (replace with actual logic)
    image_file = request.files.get('image')

    if image_file:
        # Save the image to a temporary location or use in-memory processing
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
        image_file.save(image_path)

        # Call the model1 function to perform text recognition
        text, audio_file, adjusted_image_path, timestamp = text_recognition_upload.perform_ocr_and_audio(image_path)


        # Process the results (e.g., display text, play audio)
        return render_template('text-recognition-upload.html', text=text, audio_file=audio_file, adjusted_image_path=adjusted_image_path, timestamp=timestamp)

    else:
        return render_template('text-recognition-upload.html', error="Please upload an image.")


@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)




@app.route('/text2')
def text2():
      return render_template('text-recognition-capture.html')


@app.route('/text-capture', methods=['POST'])
def text_capture():
    text_output, img_path, audio_path, timestamp = text_recognition_capture.perform_text_capture()
    return render_template('text-recognition-capture.html', text_output=text_output, img_path=img_path, audio_path=audio_path, timestamp=timestamp)

    

@app.route('/text3')
def text3():
    return render_template('text-recognition-live.html')


@app.route('/text-live', methods=['POST'])
def text_live():
    
    text = text_recognition_live.perform_live_text()

    return render_template('text-recognition-live.html', text=text )



@app.route('/object')
def object():
    return render_template('object-detection.html')


@app.route('/object1')
def object1():
    return render_template('object-detection-upload.html')


@app.route('/object-upload', methods=['POST'])
def object_upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Call the object detection and generate audio description
        detection_result, audio_path, timestap = object_detection_upload.detect_objects(file_path)
        
        # Get paths for displaying results
        audio_file = os.path.basename(audio_path)
        
        return render_template('object-detection-upload.html', detection_result=detection_result, audio_file=audio_file, timestap=timestap)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)


@app.route('/object2')
def object2():
    return render_template('object-detection-capture.html')


@app.route('/object-capture')
def object_capture():

    description_text, img_filename, audio_filename = object_detection_capture.perform_object_detection()

    # Render a template with the detection results and paths to the image and audio file
    return render_template('object-detection-capture.html', description_text=description_text, img_filename=img_filename, audio_filename=audio_filename)


@app.route('/give_image/<filename>')
def give_image(filename):
    return send_from_directory('static/captured', filename)

@app.route('/give_audio/<filename>')
def give_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)


@app.route('/object3')
def object3():
    return render_template('object-detection-live.html')


@app.route('/object-live', methods=['POST'])
def object_live():
    
    detected_objects = object_detection_live.object_detection()

    return render_template('object-detection-live.html',  detected_objects=detected_objects )



if __name__ == '__main__':
    app.run(debug=True)
