import cv2
import os
import random
import argparse
import numpy as np

# params to set
types = ["palm", "fist", "right", "left", "up", "down", "other"]

num_per_set = 1000

bgr_low = (0, 150, 0)
bgr_high = (50, 255, 50)
image_buffer_directory = "imageBuffer/"

# entry point
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder")
    args = parser.parse_args()

    folder = args.output_folder
    if os.path.isdir(folder):
        print("Folder {} already exists! Aborting...".format(folder))
        return
    else:
        print("Making data folder...")
        os.makedirs(folder)

    curr_type = 0
    count = 0

    print("Starting at {}\n".format(types[0]))

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
        #mask = cv2.inRange(frame, bgr_low, bgr_high) 

        cv2.imshow("frame", frame)
        #cv2.imshow("mask", mask)

        key = cv2.waitKey(30)

        if key == ord('q'):
            break

        if key == 32: # space
            if count == 0:
                os.makedirs("{}/{}".format(folder, types[curr_type]))

            path = "{}/{}/image_{:03d}.jpg".format(folder, types[curr_type], count)
            print("Saving to {}".format(path))
            cv2.imwrite(path, frame)

            if count == num_per_set - 1:
                curr_type += 1
                if curr_type == len(types):
                    break
                print("\nNow switching to: {}\n".format(types[curr_type]))
                count = 0
            else:
                count += 1

if __name__ == "__main__":
    main()
