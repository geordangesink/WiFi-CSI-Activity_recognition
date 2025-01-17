import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Define the base path to your images
base_path = './images/3/combined/body_movements'

# Check if the base path exists
if not os.path.exists(base_path):
    raise FileNotFoundError(f"Base path does not exist: {base_path}")

# Remove hidden files (e.g., .DS_Store, ., ..)
def remove_hidden_files(base_path):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.startswith('.'):  # Exclude hidden files
                file_path = os.path.join(root, file)
                print(f"Removing hidden file: {file_path}")
                os.remove(file_path)

remove_hidden_files(base_path)

# Parameters
IMG_SIZE = (128, 2000)  # Adjust the size to what works for your data
BATCH_SIZE = 32
RANDOM_STATE = 42

# Data Preprocessing using ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.1)

# Load train and validation sets (90% for training, 10% for validation)
train_set = train_datagen.flow_from_directory(
    base_path,
    target_size=IMG_SIZE,
    color_mode="rgb",
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="training",
    shuffle=True,
    seed=RANDOM_STATE
)

validation_set = train_datagen.flow_from_directory(
    base_path,
    target_size=IMG_SIZE,
    color_mode="rgb",
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="validation",
    shuffle=True,
    seed=RANDOM_STATE
)

# Build the CNN model
Classifier = Sequential()
Classifier.add(Convolution2D(32, (3, 3), input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)))
Classifier.add(LeakyReLU(alpha=0.1))
Classifier.add(MaxPooling2D(pool_size=(2, 2)))
Classifier.add(Dropout(0.25))
Classifier.add(Flatten())
Classifier.add(Dense(128, activation='relu'))
Classifier.add(Dropout(0.1))
Classifier.add(Dense(len(train_set.class_indices), activation='softmax'))

# Compile the model
Classifier.compile(optimizer=Adam(learning_rate=0.0001),
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])

# Train the model
history = Classifier.fit(
    train_set,
    epochs=20,
    validation_data=validation_set
)

# Save the model
Classifier.save('motion_classifier_model.keras')
print("Model saved as 'motion_classifier_model.keras'.")

# Plot training history
plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.title('Loss over Epochs')
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')
plt.subplot(1, 2, 2)
plt.title('Accuracy over Epochs')
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.savefig('training_history_channel3-body_movements.png', dpi=300, bbox_inches='tight')
plt.show()
