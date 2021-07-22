# This file contains the test for the find_char functionality

import cv2
from ..src.char_detection import find_char
from ..src.char_detection import img_preprocess

def test_find_char():

   img = cv2.imread('../inputs/test-word.jpeg', 0)

   dst = img_preprocess(img)

   bbox_list, traces_list = find_char(dst)

   assert len(bbox_list) == len(traces_list) == 7
