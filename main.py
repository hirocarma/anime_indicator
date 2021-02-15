#!/usr/bin/env python
import sys
import os

import histogram
import feature
import hash

_, IMG_DIR, IMG_OUT_DIR = sys.argv

files = os.listdir(IMG_DIR)
files = sorted(files)
frame_cnt = len(files)

#histogram
diff, cnt, scene_cnt = histogram.hist(IMG_DIR, files, IMG_OUT_DIR)

diff = diff / float(frame_cnt)
print('histogram_diff: %s' % (diff))
print('histogram_cnt: %s' % (cnt))
print('scene_cnt: %s' % (scene_cnt))

sys.exit()

#feature
diff, between_diff, key_diff, cnt, between_cnt, key_cnt = \
    feature.feature(IMG_DIR, files, IMG_OUT_DIR)

diff = diff / float(frame_cnt)
between_diff = between_diff / float(frame_cnt)
key_diff = key_diff / float(frame_cnt)

print('feature_diff(all): %s' % (diff))
print('feature_diff(between): %s' % (between_diff))
print('feature_diff(key): %s' % (key_diff))

print('feature_cnt(all): %s' % (cnt))
print('feature_cnt(between): %s' % (between_cnt))
print('feature_cnt(key): %s' % (key_cnt))

#hash
cnt = hash.hash(IMG_DIR, files, IMG_OUT_DIR)
print('hash_cnt: %s' % (cnt))

cnt = hash.hash_all(IMG_DIR, files)
print('hash_cnt(comp_all): %s' % (cnt))

#frame
print('frame_count: %s' % (frame_cnt))
