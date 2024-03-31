
import torch
from PIL import Image
from gtts import gTTS
import os


# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Load an image
img_path = r'C:\Users\Home\Downloads\ani.jpg'  # Update this to the path of your image
img = Image.open(img_path)

# Inference
results = model(img)

# Results
print("detected objects :: ")
results.print()  # Print results to console

# Display image with bounding boxes, labels, and scores
results.show()

rendered_img = results.render()[0]  # results.render() returns a list of images

# Convert the rendered image back to a PIL image (from bytes)
detected_img = Image.fromarray(rendered_img)

# Specify your desired save path
save_path = 'C:\\Users\\Home\\Downloads\\output.jpg'

# Save the image
detected_img.save(save_path)

print(f"Saved detected image to {save_path}")



