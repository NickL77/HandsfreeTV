import os
import cv2

bgr_low = (0, 150, 0)
bgr_high = (50, 255, 50)

while True:
    image_buffer_directory = 'imageBuffer/'

    recent_1 = []
    recent_2 = []

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
                replace[1] = time

    frame = cv2.imread(recent_1[0])
    if frame is None:
        continue
    height, width, channels = frame.shape
    if height == 0 or width == 0:
        continue

    mask = cv2.inRange(frame, bgr_low, bgr_high)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)

    key = cv2.waitKey(30)

    if key == ord("q"):
        break
