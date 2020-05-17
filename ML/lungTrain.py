import librosa
import tensorflow as tf
import numpy as np
import pandas as pd
import glob
from tensorflow.keras import models, datasets, optimizers, utils, layers
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
from sklearn.model_selection import train_test_split

# Put this file in the Respiratory_Sound_Database directory on the same level as patient_diagnosis.csv
# Exclude Asthma and LRTI since not enough training data

EPOCHS = 250
BATCH_SIZE = 256

PAD_SIZE = 862 #Most have a size of 862, skip anything bigger

def get_mfccs(filename):
    
    try:
        a, sr = librosa.load(filename)
        mfccs = librosa.feature.mfcc(y=a, sr=sr, n_mfcc=40)
        #print(mfccs.shape[1])
        padding = PAD_SIZE - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, padding)), mode='constant')

    except Exception as e:
        print("Error, skipping file ", filename)
        return None

    return mfccs

patientNums = []
features = []

# Read in audio files and extract mfccs
for fileName in glob.glob("./audio_and_txt_files/*.wav"):
    mfccs = get_mfccs(fileName)
    #mfccs = 1
    #print(mfccs.shape)
    if mfccs is not None:
        patientNums.append(fileName[22:25])
        features.append(mfccs)

patientNums = np.array(patientNums)

features = np.array(features)

metadata = pd.read_csv("patient_diagnosis.csv", header=None)
labels = []

#Convert patient id's to class labels
for patientId in patientNums:
    print(patientId)
    labels.append(metadata[metadata[0] == int(patientId)].iloc[0][1])

labels = np.array(labels)
print(labels.shape)
print(labels)
#Remove classes that have barely any training data

print(features.shape)

features = np.delete(features, np.where((labels == 'Asthma') | (labels == 'LRTI'))[0], axis=0)
labels = np.delete(labels, np.where((labels == 'Asthma') | (labels == 'LRTI'))[0], axis=0)

le = LabelEncoder()
transLabel = tf.keras.utils.to_categorical(le.fit_transform(labels))

#['Bronchiectasis', 'Bronchiolitis', 'COPD', 'Healthy', 'Pneumonia', 'URTI']
#print(list(le.classes_))

#Reshape to fit into CNN
features = np.reshape(features, (*features.shape, 1))
print(features.shape)

# .80 .20 split
x_train, x_test, y_train, y_test = train_test_split(features, transLabel, test_size=0.2, random_state = 42)

# Define CNN architecture
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(filters=16, kernel_size=2,input_shape=(40,  862, 1), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))

model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=2, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))

model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=2, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))

model.add(tf.keras.layers.Conv2D(filters=128, kernel_size=2, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.2))

model.add(tf.keras.layers.GlobalAveragePooling2D())

model.add(tf.keras.layers.Dense(6, activation='softmax')) 

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam') 

model.summary()

# Pretraining accuracy
score = model.evaluate(x_test, y_test, verbose=1)
accuracy = 100*score[1]
print("Pre-training accuracy: %.4f%%" % accuracy)

start = datetime.now()

#Train
model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(x_test, y_test),  verbose=1)


duration = datetime.now() - start
print("Training time: ", duration)

score = model.evaluate(x_train, y_train, verbose=0)
print("Training Accuracy: ", score[1])

score = model.evaluate(x_test, y_test, verbose=0)
print("Testing Accuracy: ", score[1])

model.save("breathing_model")
