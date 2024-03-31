
import torch
import cv2
from transformers import GPT2Tokenizer, GPT2LMHeadModel



# Function to load the YOLOv5 model
def load_yolov5_model(model_name='yolov5s', device='cuda'):
    model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)
    model.to(device).eval()
    return model

# Function for object detection
def detect_objects(model, img_path, device='cuda'):
    img = cv2.imread(img_path)
    results = model(img)
    labels = results.names
    detected_objects = [labels[int(x)] for x in results.xyxy[0][:, -1]]
    return detected_objects

# Function to generate text with GPT-2
def generate_text(descriptions, model_name='gpt2', max_length=100):
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    prompt = "This image contains objects such as " + ", ".join(descriptions) + "."
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Main function to run the detection and text generation
def main(img_path):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    yolov5_model = load_yolov5_model(device=device)
    detected_objects = detect_objects(yolov5_model, img_path, device)
    if detected_objects:
        description_text = generate_text(detected_objects)
        print(f"Detected Objects: {detected_objects}")
        print(f"Generated Description: {description_text}")
    else:
        print("No objects detected.")


if __name__ == "__main__":
    image_path = r'C:\Users\Home\Downloads\images.jpg'  # Update this to the path of your image
    main(image_path)




