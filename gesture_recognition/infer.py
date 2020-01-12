import cv2
import random
import glob
import tensorflow as tf
import os
import numpy as np

# params to set
types = ["palm", "fist", "right", "left", "up", "down", "other"]

bgr_low = (0, 150, 0)
bgr_high = (50, 255, 50)
image_buffer_directory = "imageBuffer/"

# entry point
def main():

    model = tf.keras.models.load_model("old_model.h5")

    recent_1 = []
    recent_2 = []

    while True:

        images = os.listdir(image_buffer_directory)
        for i in range(len(images)):

            f = image_buffer_directory + images[i]
            time = os.path.getmtime(f)

            if i == 0:
                recent_1 = [f, time]
            elif i == 1:
                recent_2 = [f, time]
            else:
                replace = min([recent_1, recent_2], key=lambda x: x[1])
                if replace[1] < time:
                    replace[0] = f
                    replace[1]

        frame = cv2.imread(recent_1[0])

        if frame is None:
            continue
        h, w, c = frame.shape
        if h == 0 or w == 0:
            continue

        cv2.imshow("frame", frame)
        frame = cv2.inRange(frame, bgr_low, bgr_high)

        resized = cv2.resize(frame, (240, 180))
        r = np.expand_dims(resized.reshape(resized.shape + (1, )), axis=0)

        pred = model.predict_classes(r)
        print(pred)

        cv2.imshow("mask", frame)
        cv2.imshow("resized", resized)

        key = cv2.waitKey(30)
        if key == ord('q'):
            break

if __name__ == "__main__":
    main()
