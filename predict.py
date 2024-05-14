import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from PIL import Image
import cv2
import glob
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub


input_image_path = 'static/images/dog.jpg'

input_image = cv2.imread(input_image_path)

# cv2.imshow(input_image)

input_image_resized = cv2.resize(input_image, (224, 224))

input_image_scaled = input_image_resized/255

image_reshaped = np.reshape(input_image_scaled, [1, 224, 224, 3])

# load model
filename = 'finalized_model.keras'
model = keras.models.load_model(filename)

# run on image
input_prediction = model.predict(image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)

print(input_pred_label)

if input_pred_label == 0:
  print('The image shows a cat')
else:
  print('The image shows a dog')