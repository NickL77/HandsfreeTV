import cv2
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("data_folder")

args = parser.parse_args()
data_folder = args.data_folder

for f in list(glob.glob("{}/*.jpg".format(data_folder))):
    frame = cv2.imread(f)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("frame", gray)
    cv2.waitKey(30)
