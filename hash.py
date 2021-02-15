#!/usr/bin/env python
import cv2
from PIL import Image
import imagehash

DEBUG = 0
WRITE = 1

def hash(IMG_DIR, files, IMG_OUT_DIR):

    diff = between_diff = key_diff = 0
    prev = between_prev = key_prev = 0
    cnt = between_cnt = key_cnt = 0

    prev_img_path = IMG_DIR + files[0]
    prev_hash = imagehash.phash(Image.open(prev_img_path))

    for file in files:
        comparing_img_path = IMG_DIR + file
        comparing_hash = imagehash.phash(Image.open(comparing_img_path))
        if prev_hash != comparing_hash:
            cnt = cnt + 1
            prev_hash = comparing_hash
            if DEBUG == 1:
                print(file, ret, diff)
    return cnt

def hash_all(IMG_DIR, files):
    cnt = 0
    imgs = {}
    for img in files:
        img_path = IMG_DIR + img
        hash = imagehash.phash(Image.open(img_path))
        if hash in imgs:
            if DEBUG == 1:
                print('Similar image :', img, imgs[hash])
        else:
            imgs[hash] = img
            cnt = cnt + 1
            if DEBUG == 1:
                comparing_img = cv2.imread(img_path)
                z_key_cnt = str(cnt).zfill(5)
                cv2.imwrite(IMG_OUT_DIR + 'hash_between' + z_key_cnt + '.jpg', comparing_img)
    return cnt
