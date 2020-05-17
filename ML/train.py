import librosa, librosa.display
import matplotlib.pyplot as plt
import glob, os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets, models, optimizers, utils, layers
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from datetime import datetime

#Put this file in the same directory as the .csv files

EPOCHS = 1000
BATCH_SIZE = 256

#metadata.csv is a metadata file I created containing the labeled training data from both set A
#I think set B metadata file is broken or something
metadata = pd.read_csv("metadata.csv")

#Get the max columns in order to find the padding
def findMaxSize():

    mfccSize = []

    for index, row in metadata.iterrows():
        fileName = os.path.join(os.getcwd(), str(row['fname']))
        print(fileName)
        a, sr = librosa.load(fileName)
        mfccs = librosa.feature.mfcc(y=a, sr=sr)
        mfccSize.append(mfccs.shape[1])

    print("Max Size: {}".format(max(mfccSize)))

#findMaxSize()

PAD_SIZE = 388

#Get mfccs of .wav and pad it if necessary
def get_mfccs(filename):
    a, sr = librosa.load(filename)
    mfccs = librosa.feature.mfcc(y=a, sr=sr, n_mfcc=40)
    padding = PAD_SIZE - mfccs.shape[1]
    mfccs = np.pad(mfccs, pad_width=((0, 0), (0, padding)), mode='constant')

    return mfccs

# x is list of features, y is list of classes
x = []
y = []

#Extract mfccs and class names
for index, row in metadata.iterrows():
    fileName = os.path.join(os.getcwd(), str(row['fname']))
    mfccs = get_mfccs(fileName)
    x.append(mfccs)
    y.append(str(row['fname']).split("__")[0])

#Map class labels to numbers
le = LabelEncoder()
yy = tf.keras.utils.to_categorical(le.fit_transform(y))
print(list(le.classes_))

# .80 .20 train test split
xTrain, xTest, yTrain, yTest = train_test_split(np.array(x), np.array(yy), test_size=.2, random_state=42)

print("\n\ntrain size: {}".format(len(xTrain)))
print("test size: {}".format(len(xTest)))

rows = 40
cols = 388

#Reshaping input data to fit into CNN
xTrain = xTrain.reshape(xTrain.shape[0], rows, cols, 1)
xTest = xTest.reshape(xTest.shape[0], rows, cols, 1)

print("\ntrain shape: {}\n\n".format(xTrain.shape))

#Defining CNN architecture
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(filters=16, kernel_size=2, input_shape=(rows, cols, 1), activation='relu'))
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

model.add(tf.keras.layers.Dense(4, activation='softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

model.summary()

#pre-training accuracy
score = model.evaluate(xTest, yTest, verbose=1)
accuracy = 100*score[1]

print("Pre-training accuracy: %.4f%%" % accuracy)

start = datetime.now()

#Train it
model.fit(xTrain, yTrain, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(xTest, yTest), verbose=1)

print("Training time: {}".format(datetime.now() - start))

#Evaluate model on train and test data
score = model.evaluate(xTrain, yTrain, verbose=0)
print("Training Accuracy: ", score[1])

score = model.evaluate(xTest, yTest, verbose=0)
print("Testing Accuracy: ", score[1])

model.save("model")
