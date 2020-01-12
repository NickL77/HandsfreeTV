import cv2
import random
import glob
import tensorflow as tf
import os, sys
import numpy as np
import collections
import time

sys.path.append(os.path.abspath('../YTControl'))

from YTControl import YTControl

types = ["palm", "fist", "right", "left", "up", "down", "other"]

green_low = (0, 150, 0)
green_hi = (50, 255, 50)
red_low = (0, 0, 150)
red_hi = (50, 50, 255)

image_buffer_directory = "/home/nick/Programming/handsfreeTV/gesture_recognition/image_buffer/"

ring_buf = collections.deque(maxlen=5)

def valid_entry():
    if not len(ring_buf) == 5:
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
# def main():

def gesture_thread(yt):

    model = tf.keras.models.load_model("/home/nick/Programming/handsfreeTV/gesture_recognition/model.h5")

    recent_1 = []
    recent_2 = []
    prev_time = 0
    reading = ''

    while True:

        images = os.listdir(image_buffer_directory)
        for i in range(len(images)):

            f = image_buffer_directory + images[i]
            f_time = os.path.getmtime(f)

            if i == 0:
                recent_1 = [f, f_time]
            elif i == 1:
                recent_2 = [f, f_time]
            else:
                replace = min([recent_1, recent_2], key=lambda x: x[1])
                if replace[1] < f_time:
                    replace[0] = f
                    replace[1]

        frame = cv2.imread(recent_1[0])
        """

    for f in glob.glob("./new_data/palm/*.jpg"):
        frame = cv2.imread(f)
        print(f)
        """

        if frame is None:
            continue
        h, w, c = frame.shape
        if h == 0 or w == 0:
            continue


        green_mask = cv2.inRange(frame, green_low, green_hi)
        red_mask = cv2.inRange(frame, red_low, red_hi)
        mask = green_mask + red_mask

        resized = cv2.resize(mask, (240, 180))
        cv2.imshow("resized", resized)
        cv2.putText(frame, reading, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("orig", frame)

        r = np.expand_dims(resized.reshape(resized.shape + (1, )), axis=0)

        pred = model.predict_classes(r)
        pred = int_to_type(pred)
        ring_buf.append(pred)

        if valid_entry():
            gesture = ring_buf[1]
            reading = gesture
            print(gesture)

            if time.time() - prev_time > 2:
                
                if gesture == 'fist':
                    yt.pause()
                elif gesture == 'palm':
                    yt.play()
                elif gesture == 'up':
                    yt.volume_up()
                elif gesture == 'down':
                    yt.volume_down()

                print('action taken')
                prev_time = time.time()

                
        key = cv2.waitKey(30)
        if key == ord('q'):
            break

#if __name__ == "__main__":
#    main()
