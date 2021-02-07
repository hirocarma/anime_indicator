#!/usr/bin/env python

import sys
import os
import cv2
import numpy as np

_, IMG_DIR, IMGFILE_CNT = sys.argv

DEBUG = 0

target_img=np.zeros((270, 480, 3), np.uint8)
cv2.rectangle(target_img, (10, 10), (100, 100), (0,255,0), 5)

files = os.listdir(IMG_DIR)
files = sorted(files)

target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])
diff = 0
prev = 1
for file in files:
    comparing_img_path = IMG_DIR + file
    comparing_img = cv2.imread(comparing_img_path)
    comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])

    ret = cv2.compareHist(target_hist, comparing_hist, 0)
    diff = diff + abs(prev - ret)
    prev = ret
    if DEBUG == 1:
        print(file, ret, diff)

diff = diff / float(IMGFILE_CNT)
print('histogram_diff: %s' % (diff))

bf = cv2.BFMatcher(cv2.NORM_HAMMING)
detector = cv2.AKAZE_create()
(target_kp, target_des) = detector.detectAndCompute(target_img, None)
diff = 0
prev = 1
for file in files:
    comparing_img_path = IMG_DIR + file
    try:
        comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
        matches = bf.match(target_des, comparing_des)
        dist = [m.distance for m in matches]
        if len(dist) == 0:
            ret = 0
        else:
            ret = sum(dist) / len(dist)
    except cv2.error:
        ret = 100000
    diff = diff + abs(prev - ret)
    prev = ret
    if DEBUG == 1:
        print(file, ret, diff)

diff = diff / float(IMGFILE_CNT)
print('feature_diff: %s' % (diff))
print('frame_count: %s' % (IMGFILE_CNT))
