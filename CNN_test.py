import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

# Load the saved model
model_path = './motion_classifier_model.keras'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

model = load_model(model_path)
print("Model loaded successfully.")

# Parameters
IMG_SIZE = (128, 128)  # Ensure this matches the training size

# Path to the test dataset
test_path = './test'  # Folder containing test images
if not os.path.exists(test_path):
    raise FileNotFoundError(f"Test path does not exist: {test_path}")

# Load class labels from training process
# Replace './images/combined/gestures' with your training data path
training_base_path = './images/combined/gestures'
class_names = [folder for folder in os.listdir(training_base_path) if os.path.isdir(os.path.join(training_base_path, folder))]
class_labels = {idx: name for idx, name in enumerate(sorted(class_names))}
print(f"Class labels: {class_labels}")

# Function to predict a single image
def predict_image(image_path, model, class_labels):
    img = load_img(image_path, target_size=IMG_SIZE)  # Resize the image
    img_array = img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Add batch dim and normalize
    predictions = model.predict(img_array)
    predicted_class = int(np.argmax(predictions, axis=1)[0])  # Get class index as int
    predicted_label = class_labels[predicted_class]
    return predicted_label, predictions[0]

# Predict for all images in the test folder
def predict_all_in_test_path(test_path, model, class_labels):
    for file in os.listdir(test_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(test_path, file)
            predicted_label, probabilities = predict_image(image_path, model, class_labels)
            print(f"Image: {file}")
            print(f"Predicted Label: {predicted_label}")
            print(f"Class Probabilities: {probabilities}")
            img = load_img(image_path)
            plt.imshow(img)
            plt.title(f"Predicted: {predicted_label}")
            plt.axis('off')
            plt.show()

# Run predictions
predict_all_in_test_path(test_path, model, class_labels)
