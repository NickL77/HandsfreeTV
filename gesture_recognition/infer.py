import cv2
import random
import glob
import tensorflow as tf
import os
import numpy as np
import collections

types = ["palm", "fist", "right", "left", "up", "down", "other"]

bgr_low = (0, 150, 0)
bgr_high = (50, 255, 50)
image_buffer_directory = "imageBuffer/"

ring_buf = collections.deque(maxlen=10)

def valid_entry():
    if not len(ring_buf) == 10:
        return False
    a = ring_buf[0]
    for i in range(1, len(ring_buf)):
        if ring_buf[i] != a:
            return False
    return True

def int_to_type(i):
    if i == 0:
        return "fist"
    elif i == 1:
        return "palm"
    elif i == 2:
        return "up"
    elif i == 3:
        return "down"
    elif i == 4:
        return "left"
    elif i == 5:
        return "right"
    elif i == 6:
        return "other"
    else:
        print("WTF")
        return None

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
        pred = int_to_type(pred)
        ring_buf.append(pred)

        if valid_entry():
            print(ring_buf[1])

        cv2.imshow("mask", frame)
        cv2.imshow("resized", resized)

        key = cv2.waitKey(30)
        if key == ord('q'):
            break

if __name__ == "__main__":
    main()
