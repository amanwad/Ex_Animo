import librosa, sys
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from sklearn.preprocessing import LabelEncoder
import os
import time
from google.cloud import storage

# This program takes in a filename as a command line argument
# Loads in the keras model called "model"
# Finds MFCCs and classifies the file given by the filename

PAD_SIZE = 388
PAD_SIZE2 = 862
storage_client = storage.Client.from_service_account_json('key_copy.json')
model = tf.keras.models.load_model("model_updated")
model2 = tf.keras.models.load_model("breathing_model_updated")

#Create label encoder
le = LabelEncoder()
le.fit(["artifact", "extrahls", "murmur", "normal"])
le2 = LabelEncoder()
le2.fit(['Bronchiectasis', 'Bronchiolitis', 'COPD', 'Healthy', 'Pneumonia', 'URTI'])
while(1):
    blobs = storage_client.list_blobs("aman-w_cbtvfeww4yyordijm_5-17")
    len = 0
    for blob in blobs:
        len+=1
    if(len<6):
        bucket = storage_client.get_bucket("aman-w_cbtvfeww4yyordijm_5-17")
        blob = bucket.blob("Heartbeat")
        blob.download_to_filename("heart2.wav")
        blob2 = bucket.blob("Breathing")
        blob2.download_to_filename("breathe.wav")
        filename = "heart2.wav"
        a, sr = librosa.load(filename)
        mfccs = librosa.feature.mfcc(y=a, sr=sr, n_mfcc=40)
        padWidth = PAD_SIZE - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0,0), (0,padWidth)), mode="constant")
        mfccs = mfccs.reshape(1, 40, 388, 1)

        #Classification
        predicted_vector = model.predict_classes(mfccs)
        predicted_class = le.inverse_transform(predicted_vector)

        predicted_proba_vector = model.predict_proba(mfccs)
        predicted_proba = predicted_proba_vector[0]

        print("\n\nThe predicted class is:", predicted_class[0], '\n')
        f = open("ML.txt", "w")
        f.write("The predicted class for the hearbeat file is: ")
        f.write(predicted_class[0])
        f.write("\n")
        f.write(str(predicted_proba_vector[0]))
        filename = "breathe.wav"
        a2, sr2 = librosa.load(filename)
        mfccs = librosa.feature.mfcc(y=a2, sr=sr2, n_mfcc=40)
        padWidth = PAD_SIZE2 - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0,0), (0,padWidth)), mode="constant")
        mfccs = mfccs.reshape(1, 40, PAD_SIZE2, 1)

        #Classification
        predicted_vector = model2.predict_classes(mfccs)
        predicted_class = le2.inverse_transform(predicted_vector)
        print("\n\nThe predicted class is:", predicted_class[0], '\n')

        predicted_proba_vector = model2.predict_proba(mfccs)
        predicted_proba = predicted_proba_vector[0]
        f.write("\nThe predicted class for the lung file is: ")
        f.write(predicted_class[0])
        f.write("\n")
        f.write(str(predicted_proba_vector[0]))
        f.close()
        blob = bucket.blob("ML")
        blob.upload_from_filename("ML.txt")
        time.sleep(10)

#Load model


#Get mfccs
filename = "untitled.wav"
a, sr = librosa.load(filename)
mfccs = librosa.feature.mfcc(y=a, sr=sr, n_mfcc=40)
padWidth = PAD_SIZE - mfccs.shape[1]
mfccs = np.pad(mfccs, pad_width=((0,0), (0,padWidth)), mode="constant")
mfccs = mfccs.reshape(1, 40, 388, 1)

#Classification
predicted_vector = model.predict_classes(mfccs)
predicted_class = le.inverse_transform(predicted_vector)
print("\n\nThe predicted class is:", predicted_class[0], '\n')

predicted_proba_vector = model.predict_proba(mfccs)
predicted_proba = predicted_proba_vector[0]

for i in range(len(predicted_proba)):
    category = le.inverse_transform(np.array([i]))
    print(category[0], "\t : ", format(predicted_proba[i], '.32f') )
