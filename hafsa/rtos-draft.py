import tensorflow as tf
import keras
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.layers import TFSMLayer
import cv2  # Ensure you have opencv-python installed
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model using TFSMLayer
model = tf.keras.Sequential([
    TFSMLayer('./model.savedmodel', call_endpoint='serving_default')
])

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height, 224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the model's input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predict with the model
    prediction_dict = model(image, training=False)
    # Assuming 'output_0' is the key for the output tensor
    prediction = prediction_dict['sequential_3'].numpy()

    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name.strip(), end=" ")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
