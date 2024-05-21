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
import urllib


# TODO: error on model load. Need to register custom objects.
'''
Error message:
ValueError: Unknown layer: 'KerasLayer'. Please ensure you are using a `keras.utils.custom_object_scope` and that this object is included in the scope.
 See https://www.tensorflow.org/guide/keras/save_and_serialize#registering_the_custom_object for details.

'''

#export_path = '/tmp/saved_models/1715765253'
export_path = 'savedModel'
reloaded = tf.keras.models.load_model(export_path)

def predict(input_image_url = 'https://res.cloudinary.com/ddfqaz73q/image/upload/f_auto,q_auto/download_cr75sh'):
    
    #input_image = cv2.imread(input_image_path)
    url_response = urllib.request.urlopen(input_image_url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    input_image = cv2.imdecode(img_array, -1)
    
    # cv2.imshow(input_image)
    
    input_image_resized = cv2.resize(input_image, (224, 224))
    
    input_image_scaled = input_image_resized/255
    
    image_reshaped = np.reshape(input_image_scaled, [1, 224, 224, 3])
    
    # run on image
    input_prediction = reloaded.predict(image_reshaped)
    
    input_pred_label = np.argmax(input_prediction)
    
    cat_or_dog = ''
    
    if input_pred_label == 0:
      cat_or_dog = 'cat'
    else:
      cat_or_dog = 'dog'
      
      
    return cat_or_dog