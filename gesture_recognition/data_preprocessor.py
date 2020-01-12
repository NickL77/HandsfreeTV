import argparse
import cv2
import sys
import os
import glob
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("recorded_data_folder")

args = parser.parse_args()
data_folder = args.recorded_data_folder

output_folder = "processed_{}".format(data_folder)

if os.path.isdir(output_folder):
    print("{} already exists! aborting...".format(output_folder))
    sys.exit(1)

os.makedirs(output_folder)
os.makedirs("{}/frames".format(output_folder))
os.makedirs("{}/labels".format(output_folder))

curr_frame = 0

# bgr
green_low = (0, 150, 0)
green_hi = (50, 255, 50)
red_low = (0, 0, 150)
red_hi = (50, 50, 255)

folders = [os.path.join(data_folder, o) for o in os.listdir(data_folder)
        if os.path.isdir(os.path.join(data_folder, o))]

for folder in folders:
    for f in glob.glob("{}/*.jpg".format(folder)):
        # default copy
        frame = cv2.imread(f)
        green_mask = cv2.inRange(frame, green_low, green_hi)
        red_mask = cv2.inRange(frame, red_low, red_hi)
        mask = green_mask + red_mask

        resized = cv2.resize(mask, (240, 180))

        cv2.imwrite("{}/frames/{:03d}.jpg".format(output_folder, curr_frame), resized)
        label_file = open("{}/labels/{:03d}.txt".format(output_folder, curr_frame), "w")
        label = folder.split("/")[1]
        label_file.write(label)
        label_file.close()
        curr_frame += 1

print("Done!")
