#!/usr/bin/env python
import cv2
import numpy as np

DEBUG = 1
WRITE = 1

def hist(IMG_DIR, files, IMG_OUT_DIR):

    diff = prev = cnt = 0
    scene_prev = scene_cnt = 0

    target_img = prev_img = np.zeros((270, 480, 3), np.uint8)
    target_histB = cv2.calcHist([target_img], [0], None, [256], [0, 256])
    target_histG = cv2.calcHist([target_img], [1], None, [256], [0, 256])
    target_histR = cv2.calcHist([target_img], [2], None, [256], [0, 256])
    for file in files:
        comparing_img_path = IMG_DIR + file
        comparing_img = cv2.imread(comparing_img_path)
        comparing_histB = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])
        comparing_histG = cv2.calcHist([comparing_img], [1], None, [256], [0, 256])
        comparing_histR = cv2.calcHist([comparing_img], [2], None, [256], [0, 256])

        retB = cv2.compareHist(target_histB, comparing_histB, cv2.HISTCMP_CORREL)
        retG = cv2.compareHist(target_histG, comparing_histG, cv2.HISTCMP_CORREL)
        retR = cv2.compareHist(target_histR, comparing_histR, cv2.HISTCMP_CORREL)
        ret = 1 - ((retB + retG + retR) / 3)  # 0 to 2

#        if ret < 1.006:
#            continue
        diff = diff + ret
        if abs(prev - ret) > 0:
            if DEBUG == 1:
                print(file, ret, abs(prev - ret), diff)
            cnt = cnt + 1
            prev = ret

        else:
            if WRITE == 1:
                cv2.imwrite(IMG_OUT_DIR + 'eq' + str(cnt).zfill(5) + '.jpg', comparing_img)
            continue
        #scene frame
        if abs(scene_prev - ret) > 0.15:
            if WRITE == 1:
                z_scene_cnt = str(scene_cnt).zfill(5)
                cv2.imwrite(IMG_OUT_DIR + 'scene' + z_scene_cnt + '.jpg', prev_img)
                if DEBUG == 1:
                    print('scene', file, ret, abs(scene_prev - ret), diff)
            scene_cnt = scene_cnt + 1
            scene_prev = ret
            prev_img = comparing_img
            
    return diff, cnt, scene_cnt

