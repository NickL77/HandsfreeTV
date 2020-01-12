import os
import cv2
import shutil

'''
move images that we do not want to be detected into the others directoru
'''

data_dir = './data1/'
paths = ['fist/', 'palm/', 'right/', 'left/', 'up/', 'down/']
negatives = data_dir + 'other/'
neg_i = len(os.listdir(negatives))

for p in paths:
    for img in os.listdir(data_dir + p):

        img_path = data_dir + p + img
        print(img_path)

        frame = cv2.imread(img_path)
        cv2.imshow('frame', frame)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('n'):
                break
            elif key == ord('d'):
                other_img_name = negatives + str(neg_i) + '.jpg'
                shutil.move(img_path, other_img_name)
                neg_1 += 1
                break



