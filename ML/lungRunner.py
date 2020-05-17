import librosa, sys
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from sklearn.preprocessing import LabelEncoder
import os

# This program takes in a filename as a command line argument
# Loads in the keras model called "model"
# Finds MFCCs and classifies the file given by the filename

PAD_SIZE = 862

#Load model
model = tf.keras.models.load_model("breathing_model_updated")

#Create label encoder
le = LabelEncoder()
le.fit(['Bronchiectasis', 'Bronchiolitis', 'COPD', 'Healthy', 'Pneumonia', 'URTI'])

#Get mfccs
filename = "breath4.wav"
a, sr = librosa.load(filename)
mfccs = librosa.feature.mfcc(y=a, sr=sr, n_mfcc=40)
padWidth = PAD_SIZE - mfccs.shape[1]
mfccs = np.pad(mfccs, pad_width=((0,0), (0,padWidth)), mode="constant")
mfccs = mfccs.reshape(1, 40, PAD_SIZE, 1)

#Classification
predicted_vector = model.predict_classes(mfccs)
predicted_class = le.inverse_transform(predicted_vector)
print("\n\nThe predicted class is:", predicted_class[0], '\n')

predicted_proba_vector = model.predict_proba(mfccs)
predicted_proba = predicted_proba_vector[0]

for i in range(len(predicted_proba)):
    category = le.inverse_transform(np.array([i]))
    print(category[0], "\t : ", format(predicted_proba[i], '.32f') )
