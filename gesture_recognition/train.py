import tensorflow as tf
import numpy as np
import random
import cv2
import os
from tensorflow.keras import datasets, layers, models

model = models.Sequential()
model.add(layers.Conv2D(32, (5, 5), activation='relu', input_shape=(180, 240, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(0.25))
model.add(layers.Flatten())
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dropout(0.25))
model.add(layers.Dense(7, activation='softmax'))

model.summary()

model.compile(optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

training_dir = "./processed_data/"
frames_dir = training_dir + "frames"
labels_dir = training_dir + "labels"

def string_to_int(s):
    if s == "fist":
        return 0
    elif s == "palm":
        return 1
    elif s == "up":
        return 2
    elif s == "down":
        return 3
    elif s == "left":
        return 4
    elif s == "right":
        return 5
    elif s == "other":
        return 6
    else:
        print("WTF")
        return None

def create_training_data():
    training_data = []
    for img in os.listdir(frames_dir):
        i = img[:len(img)-4]

        img_array = cv2.imread(os.path.join(frames_dir, img), 0)
        img_array = img_array.reshape(img_array.shape + (1,))

        f = open(os.path.join(labels_dir, str(i) + '.txt'), 'r')
        label = string_to_int(f.read())
        f.close()

        training_data.append([img_array, label])

    random.shuffle(training_data)

    X = []
    y = []
    for feat, label in training_data:
        X.append(feat)
        y.append(label)
    X = np.array(X)
    y = np.array(y)
    return X, y

X, y = create_training_data()

callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10),
             tf.keras.callbacks.ModelCheckpoint(filepath='model.h5', monitor='val_loss', save_best_only=True)]
model.fit(X, y, batch_size=64, epochs=100, validation_split=0.3, callbacks=callbacks, shuffle=True)

model.save("model.h5")
