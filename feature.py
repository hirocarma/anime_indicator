#!/usr/bin/env python
import cv2
import numpy as np
from PIL import Image
import imagehash

DEBUG = 0
WRITE = 1

def feature(IMG_DIR, files, IMG_OUT_DIR):

    diff = between_diff = key_diff = 0
    prev = between_prev = key_prev = 0
    cnt = between_cnt = key_cnt = 0

    target_img=np.zeros((270, 480, 3), np.uint8)
    cv2.rectangle(target_img, (10,10), (100, 100), (255,255,255), 5)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)
    try:
        comparing_img_path = IMG_DIR + files[0]
        comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
        matches = bf.match(target_des, comparing_des)
        dist = [m.distance for m in matches]
        prev = sum(dist) / len(dist)
    except cv2.error:
        prev = 100
    for file in files:
        comparing_img_path = IMG_DIR + file
        try:
            comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
            (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
            matches = bf.match(target_des, comparing_des)
            dist = [m.distance for m in matches]
            ret = sum(dist) / len(dist)
        except cv2.error:
            ret = prev
        #All difference frame
        if abs(prev - ret) > 0:
            cnt = cnt + 1
            diff = diff + abs(prev - ret)
            prev = ret
            if DEBUG == 1:
                print('All', file, ret, abs(prev - ret), diff)
        #In-between frame
        if abs(between_prev - ret) > 8:
            between_cnt = between_cnt + 1
            between_diff = between_diff + abs(between_prev - ret)
            between_prev = ret
            if WRITE == 1:
                z_between_cnt = str(between_cnt).zfill(5)
                cv2.imwrite(IMG_OUT_DIR + 'between' + z_between_cnt + '.jpg', comparing_img)
            if DEBUG == 1:
                print('Between', file, ret, diff)
        #Key frame
        if abs(key_prev - ret) > 22:
            key_cnt = key_cnt + 1
            key_diff = key_diff + abs(key_prev - ret)
            key_prev = ret
            if WRITE == 1:
                z_key_cnt = str(key_cnt).zfill(5)
                cv2.imwrite(IMG_OUT_DIR + 'keyframe' + z_key_cnt + '.jpg', comparing_img)
            if DEBUG == 1:
                print('keyframe:', file, abs(prev -ret), diff )

    return diff, between_diff, key_diff, cnt, between_cnt, key_cnt
