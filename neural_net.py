# contains transfer learning neural network to classify dogs vs cats
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from PIL import Image
import cv2
import glob
import tensorflow as tf
import tensorflow_hub as hub

# counting the number of files in train folder
path, dirs, files = next(os.walk('train'))
file_count = len(files)
print('Number of images: ', file_count)

file_names = os.listdir('train')
# print(file_names)

# display dog image
# img = mpimg.imread('train/dog.2132.jpg')
# imgplt = plt.imshow(img)
# plt.show()

file_names = os.listdir('train')
cat_count = 0
dog_count = 0

for i in range(len(file_names)):
  name = file_names[i]
  if name[:3] == 'cat':
    cat_count+=1
  else:
    dog_count+=1

print(f'There are {cat_count} cat images and {dog_count} dog images')

original_folder = 'train/'
resized_folder = 'image_resized/'

# for i in range(2000):
#   filename = os.listdir(original_folder)[i]
#   img_path = original_folder+filename

#   img = Image.open(img_path)
#   img = img.resize((224,224))
#   img = img.convert('RGB')

#   newImgPath = resized_folder+filename
#   img.save(newImgPath)

# create labels for resized images: cat=0, dog=1
# create a for loop to assign labels
file_names = os.listdir('image_resized/')
labels = []

for i in range(2000):
  file_name = file_names[i]
  label = file_name[:3]

  if label == 'dog':
    labels.append(1)
  else:
    labels.append(0)

# count images of dogs and cats in this 2000: confirm distribution approx. even
values, counts = np.unique(labels, return_counts=True)
print(values)
print(counts)

# image_directory = '/content/image resized/'
image_extension = ['png', 'jpg']

files = []

[files.extend(glob.glob(resized_folder + '*.' + e)) for e in image_extension]

dog_cat_images = np.asarray([cv2.imread(file) for file in files])

print(dog_cat_images.shape)

# Now use the dog_cat_images within the neural network

X = dog_cat_images
Y = np.asarray(labels)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)

print(X.shape, X_train.shape, X_test.shape)

# scaling the data
X_train_scaled = X_train/255
X_test_scaled = X_test/255

mobilenet_model = 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4'

pretained_model = hub.KerasLayer(mobilenet_model, input_shape=(224,224,3), trainable=False)

num_of_classes = 2

model = tf.keras.Sequential([
    pretained_model,
    tf.keras.layers.Dense(num_of_classes)
])

model.summary()

model.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics = ['acc']
)

model.fit(X_train_scaled, Y_train, epochs = 5)

score, acc = model.evaluate(X_test_scaled, Y_test)
print('Test Loss = ', score)
print('Test Accuracy = ', acc)

# save trained model for use on user uploads
# may be able to do this using export & load instead:
export_path = 'savedModel_2'
model.save(export_path)