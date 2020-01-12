import cv2
import handy
import os
import argparse
import numpy as np

# params to set
types = ["palm", "fist", "right", "left", "up", "down"]
num_per_set = 10

# entry point
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder")
    args = parser.parse_args()

    hist = handy.capture_histogram(source=0)
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
        hand = handy.detect_hand(frame, hist)

        cv2.imshow("hand", hand.outline)

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
