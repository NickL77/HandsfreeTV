import cv2
import os
import argparse
import numpy as np

# flags to set
types = ["palm", "fist", "point_right", "point_left", "point_up", "point_down", "other"]
num_per_set = 10
rect_top_left = (20, 50) # width, height
height, width = 220, 220
rect_bot_left = (rect_top_left[0] + width, rect_top_left[1] + height)
color = (255, 0, 0) # BGR
thickness = 2

# entry point
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder")
    args = parser.parse_args()

    cap = cv2.VideoCapture(0)

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

    while cap.isOpened():
        _, frame = cap.read()

        frame = cv2.rectangle(frame, rect_top_left, rect_bot_left, color, thickness)
        cv2.imshow("frame", frame)

        cropped_frame = frame[rect_top_left[1] : rect_top_left[1]+height, rect_top_left[0] : rect_top_left[0]+width]
        cv2.imshow("cropped_frame", cropped_frame)

        key = cv2.waitKey(30) & 0xFF

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
