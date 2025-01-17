import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# Load the saved model
model_path = './CNNs/motion_classifier_model_channel3-body_movements.keras'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

# Load class labels from training process
training_base_path = './images/3/combined/body_movements'
if not os.path.exists(training_base_path):
    raise FileNotFoundError(f"Class label path does not exist: {training_base_path}")

model = load_model(model_path)
print("Model loaded successfully.")

# Parameters
IMG_SIZE = (128, 2000)  # Ensure this matches the training size

# Path to the test dataset
test_path = './test'  # Folder containing test images
if not os.path.exists(test_path):
    raise FileNotFoundError(f"Test path does not exist: {test_path}")

# Load class labels from training process
class_names = [folder for folder in os.listdir(training_base_path) if os.path.isdir(os.path.join(training_base_path, folder))]
class_labels = {idx: name for idx, name in enumerate(sorted(class_names))}
inverse_class_labels = {v: k for k, v in class_labels.items()}  # For mapping labels to indices
print(f"Class labels: {class_labels}")

# Function to extract the ground truth label from the file name
def get_ground_truth_label(file_name):
    try:
        label = 'nothing' if file_name.split('-')[0] == 'nothing' else file_name.split('_',1)[1].split('-')[0]  # Extract the part after the first "_" and before the "-"
        return label
    except IndexError:
        return None

# Function to predict a single image
def predict_image(image_path, model, class_labels):
    img = load_img(image_path, target_size=IMG_SIZE)  # Resize the image
    img_array = img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Add batch dim and normalize
    predictions = model.predict(img_array)
    predicted_class = int(np.argmax(predictions, axis=1)[0])  # Get class index as int
    predicted_label = class_labels[predicted_class]
    return predicted_label, predictions[0]

# Predict for all images in the test folder and calculate accuracy
def evaluate_model_on_test_data(test_path, model, class_labels):
    y_true = []
    y_pred = []
    for file in os.listdir(test_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(test_path, file)
            ground_truth_label = get_ground_truth_label(file)
            if ground_truth_label is None:
                print(f"Skipping file with invalid ground truth label: {file}")
                continue
            if ground_truth_label not in inverse_class_labels:
                print(f"Ground truth label not in class labels: {ground_truth_label}")
                continue
            ground_truth_index = inverse_class_labels[ground_truth_label]
            predicted_label, _ = predict_image(image_path, model, class_labels)
            predicted_index = list(class_labels.keys())[list(class_labels.values()).index(predicted_label)]
            y_true.append(ground_truth_index)
            y_pred.append(predicted_index)

            # Display image and predictions
            img = load_img(image_path)
            plt.imshow(img)
            plt.title(f"True: {ground_truth_label}, Predicted: {predicted_label}")
            plt.axis('off')
            plt.show()

    # Calculate and print accuracy
    if y_true:
        accuracy = accuracy_score(y_true, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")

        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred, labels=list(class_labels.keys()))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(class_labels.values()))
        disp.plot(cmap='viridis', xticks_rotation='vertical')
        plt.title("Confusion Matrix")
        plt.savefig('confusion_matrix_channel3-body_movements.png', dpi=300, bbox_inches='tight')
        plt.show()
    else:
        print("No valid test samples to evaluate.")

# Run predictions and evaluation
evaluate_model_on_test_data(test_path, model, class_labels)
