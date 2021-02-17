#!/usr/bin/env python
import cv2
import numpy as np

DEBUG = 1
WRITE = 1
div = 30

def hist(IMG_DIR, files, IMG_OUT_DIR):

    score = total_score = 0
    cnt = scene_cnt = 0

    prev_img_path = IMG_DIR + files[0]
    prev_img = cv2.imread(prev_img_path)
    h, w, c = prev_img.shape
    hClp = h / div
    wClp = w / div

    for file in files:
        comp_img_path = IMG_DIR + file
        comp_img = cv2.imread(comp_img_path)
        comp_hists, scores = [[[]]], []
        for x in range(0,div):
            for y in range(0,div):
                comp_Clp = \
                    comp_img[int(y * hClp):int((y + 1) * hClp), \
                             int(x * wClp):int((x + 1) * wClp)]
                prev_Clp = \
                    prev_img[int(y * hClp):int((y + 1) * hClp), \
                             int(x * wClp):int((x + 1) * wClp)]
                color = ('b','g','r')
                for i,col in enumerate(color):
                    comp_hist = cv2.calcHist([comp_Clp],[i],None,[256],[0,256])
                    prev_hist = cv2.calcHist([prev_Clp],[i],None,[256],[0,256])
                    score = cv2.compareHist(prev_hist, comp_hist, cv2.HISTCMP_CORREL)
                    scores.append(score)
        prev_img = comp_img
        score = 1 - np.mean(scores) # 0 to 2
        total_score = total_score + score

        if score > 0 or cnt == 0:
            if DEBUG == 1:
                print(file, score, total_score)
            cnt = cnt + 1
        else:
            if WRITE == 1:
                z_cnt = str(cnt).zfill(5)
                cv2.imwrite(IMG_OUT_DIR + 'eq' + z_cnt + '.jpg', comp_img)
            if DEBUG == 1:
                print('equal:', file, score, total_score)
        #scene frame
        if score > 1:
            if WRITE == 1:
                z_scene_cnt = str(scene_cnt).zfill(5)
                cv2.imwrite(IMG_OUT_DIR + 'scene' + z_scene_cnt + '.jpg', comp_img)
            if DEBUG == 1:
                print('scene:', file, score, total_score)
            scene_cnt = scene_cnt + 1

    return total_score, cnt, scene_cnt

