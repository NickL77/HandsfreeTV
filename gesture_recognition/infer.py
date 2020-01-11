import cv2
import tensorflow as tf
import os
import numpy as np

types = ["palm", "fist", "point_right", "point_left", "point_up", "point_down", "other"]
rect_top_left = (20, 50) # width, height
height, width = 220, 220
rect_bot_left = (rect_top_left[0] + width, rect_top_left[1] + height)
color = (255, 0, 0) # BGR
thickness = 2

# entry point
def main():
    cap = cv2.VideoCapture(0)
    model = tf.keras.models.load_model("early_save.h5")

    """
    frame = cv2.imread("./processed_data/frames/000.jpg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.expand_dims(gray.reshape(gray.shape + (1, )), axis=0)
    gray = gray/255
    print(model.predict_classes(gray))

    cv2.imshow("frame", frame)

    """
    while cap.isOpened():
        _, frame = cap.read()

        frame = cv2.rectangle(frame, rect_top_left, rect_bot_left, color, thickness)
        cv2.imshow("frame", frame)

        cropped_frame = frame[rect_top_left[1] : rect_top_left[1]+height, rect_top_left[0] : rect_top_left[0]+width]
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray", gray)
        
        gray = np.expand_dims(gray.reshape(gray.shape + (1, )), axis=0)
        gray = gray/255

        key = cv2.waitKey(30) & 0xFF

        if key == ord('q'):
            break

        print(model.predict_classes(gray))

if __name__ == "__main__":
    main()
