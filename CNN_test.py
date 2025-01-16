# Import necessary libraries
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

# Load the saved model
model_path = './motion_classifier_model.keras'  # Path to your saved model
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

model = load_model(model_path)
print("Model loaded successfully.")

# Parameters
IMG_SIZE = (128, 2000)  # Ensure this matches the size used during training

# Path to the test dataset
test_path = './test'  # Replace with your test dataset folder

# Check if test path exists
if not os.path.exists(test_path):
    raise FileNotFoundError(f"Test path does not exist: {test_path}")

# Map class indices to class names
test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)
test_set = test_datagen.flow_from_directory(
    test_path,
    target_size=IMG_SIZE,
    class_mode="categorical",
    batch_size=32,
    shuffle=False,
)
class_labels = {v: k for k, v in test_set.class_indices.items()}
print(f"Class labels: {class_labels}")

# Function to predict on a single image
def predict_image(image_path, model, class_labels):
    # Load and preprocess the image
    img = load_img(image_path, target_size=IMG_SIZE)  # Resize the image
    img_array = img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image
    
    # Predict using the model
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)  # Get the class index
    
    # Get the class label
    predicted_label = class_labels[predicted_class[0]]
    return predicted_label, predictions[0]

# Predict on all images in the test path
def predict_all_in_test_path(test_path, model, class_labels):
    # Loop through all subdirectories in the test path
    for root, _, files in os.walk(test_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_path = os.path.join(root, file)
                predicted_label, probabilities = predict_image(image_path, model, class_labels)
                print(f"Image: {file}")
                print(f"Predicted Label: {predicted_label}")
                print(f"Class Probabilities: {probabilities}")
                
                # Optionally display the image with its predicted label
                img = load_img(image_path)
                plt.imshow(img)
                plt.title(f"Predicted: {predicted_label}")
                plt.axis('off')
                plt.show()

# Run the prediction for all images in the test_path
predict_all_in_test_path(test_path, model, class_labels)
