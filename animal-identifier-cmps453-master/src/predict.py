from tensorflow import keras
import tensorflow as tf
import numpy as np
import pathlib

model = keras.models.load_model('./model64.h5')

path = "./uploads/dog.jpg"

class_names = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'horse', 'sheep', 'spider', 'squirrel']

img = keras.preprocessing.image.load_img(
    path, target_size=(360, 360)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    predictions
)
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
