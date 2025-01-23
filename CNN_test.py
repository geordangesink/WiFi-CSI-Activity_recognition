import os
import random
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# Load the saved model
model_path = 'path/to/your/CNN/model'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

# Load class labels from training process (this is done by reading the names of the folders)
# alternatively you can also give a mapped list of classes
# be sure that the match the file name extracted below to compare prediction and true value
training_base_path = 'path/to/your/folder/names'
if not os.path.exists(training_base_path):
    raise FileNotFoundError(f"Class label path does not exist: {training_base_path}")

model = load_model(model_path)
print("Model loaded successfully.")

# Parameters
IMG_SIZE = (64, 1000)  # Ensure this matches the training size

# Path to the test dataset
test_path = 'path/to/your/test/data' # folder with test images
if not os.path.exists(test_path):
    raise FileNotFoundError(f"Test path does not exist: {test_path}")

# Load class labels from training process (the folder names)
class_names = [folder for folder in os.listdir(training_base_path) if os.path.isdir(os.path.join(training_base_path, folder))]
class_labels = {idx: name for idx, name in enumerate(sorted(class_names))}
inverse_class_labels = {v: k for k, v in class_labels.items()}  # For mapping labels to indices
print(f"Class labels: {class_labels}")

# extract the ground truth label from the file name
def get_ground_truth_label(file_name):
    try:
        ############### THIS SHOULD STRIP THE TESTED FILE NAME SO ONLY THE NAME EQUAL TO A CLASS NAME IS LEFT
        # for comparing accuracy
        label = 'nothing' if file_name.split('-')[0] == 'nothing' else file_name.split('_',1)[1].split('-')[0]  # Extract the part after the first "_" and before the "-"
        return label
    except IndexError:
        return None

# predict a single image
def predict_image(image_path, model, class_labels):
    img = load_img(image_path, target_size=IMG_SIZE)  # Resize the image
    img_array = img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Add batch dim and normalize
    predictions = model.predict(img_array)
    predicted_class = int(np.argmax(predictions, axis=1)[0])  # Get class index as int
    predicted_label = class_labels[predicted_class]
    return predicted_label, predictions[0]

# predict all images in the test folder and calculate accuracy
def evaluate_model_on_test_data(test_path, model, class_labels):
    y_true = []
    y_pred = []
    test_files = [file for file in os.listdir(test_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(test_files)  # Randomize file order

    for file in test_files:
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

    # Calculate and print accuracy
    if y_true:
        accuracy = accuracy_score(y_true, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")

        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred, labels=list(class_labels.keys()))
        cm_percentage = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm_percentage = np.nan_to_num(cm_percentage)

        # Plotting with fixed scale
        fig, ax = plt.subplots(figsize=(10, 10))  # Adjust size if needed
        im = ax.imshow(cm_percentage, cmap='viridis', vmin=0, vmax=1)  # Fix scale from 0 to 1
        
        # Add tick marks and labels
        ax.set_xticks(np.arange(len(class_labels)))
        ax.set_yticks(np.arange(len(class_labels)))
        ax.set_xticklabels(list(class_labels.values()), rotation=90)
        ax.set_yticklabels(list(class_labels.values()))
        plt.xlabel("Predicted")
        plt.ylabel("True")

        # Add a colorbar with the fixed scale
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("Proportion")

        # Annotate the matrix with percentage values (all numbers >= 0.5 in black, others yellow)
        for i in range(len(class_labels)):
            for j in range(len(class_labels)):
                value = cm_percentage[i, j]
                text_color = "yellow" if value < 0.5 else "black"
                ax.text(j, i, f"{value:.2g}", ha="center", va="center", color=text_color)  # fixed to 2 decimals and delete trailing 0s

        # Finalize the plot
        plt.title("Confusion Matrix")
        plt.savefig('confusion_matrix_channel3-body_movements_percentage.png', dpi=300, bbox_inches='tight')
        plt.show()
    else:
        print("No valid test samples to evaluate.")

# Run predictions and evaluation
evaluate_model_on_test_data(test_path, model, class_labels)
