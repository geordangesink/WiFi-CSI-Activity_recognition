#@title CNN
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Define the base path to your images
base_path = './images/combined/gestures'

# Check if the base path exists
if not os.path.exists(base_path):
    raise FileNotFoundError(f"Base path does not exist: {base_path}")

# Parameters
IMG_SIZE = (128, 2000)  # Adjust the input size to 778x583
BATCH_SIZE = 32
RANDOM_STATE = 42

# Define the class names, including "nobody" (add this folder structure)
class_dirs = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]

# Include "nobody" class explicitly
class_dirs.append('nobody')  # Assuming you have a folder 'nobody' in the base path

# Data Preprocessing using ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.1)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load train and validation sets (90% for training, 10% for validation)
train_set = train_datagen.flow_from_directory(
    base_path,  # Root directory
    target_size=IMG_SIZE,
    color_mode="rgb",
    class_mode="categorical",  # 'categorical' for multi-class classification
    batch_size=BATCH_SIZE,
    subset="training",  # Use the training subset (90%)
    shuffle=True,
    seed=RANDOM_STATE
)

# Load the validation set (remaining 10% of data)
validation_set = train_datagen.flow_from_directory(
    base_path,  # Root directory
    target_size=IMG_SIZE,
    color_mode="rgb",
    class_mode="categorical",  # 'categorical' for multi-class classification
    batch_size=BATCH_SIZE,
    subset="validation",  # Use the validation subset (10%)
    shuffle=True,
    seed=RANDOM_STATE
)

# Build the CNN model
Classifier = Sequential()

# First convolutional layer
Classifier.add(Convolution2D(32, (3, 3), input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)))
Classifier.add(LeakyReLU(alpha=0.1))
Classifier.add(MaxPooling2D(pool_size=(2, 2)))
Classifier.add(Dropout(0.25))

# Flattening layer
Classifier.add(Flatten())

# Fully connected layer
Classifier.add(Dense(128, activation='linear'))
Classifier.add(Dropout(0.1))

# Output layer, the number of classes is determined automatically
Classifier.add(Dense(len(train_set.class_indices), activation='softmax'))

# Compile the model
opt = Adam(learning_rate=0.0001)
Classifier.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

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

# Plot Loss
plt.subplot(1, 2, 1)
plt.title('Loss over Epochs')
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

# Plot Accuracy
plt.subplot(1, 2, 2)
plt.title('Accuracy over Epochs')
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')

plt.show()
