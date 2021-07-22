# This file contains the test for the find_char functionality

import cv2
from ..src.char_detection import find_char
from ..src.char_detection import img_preprocess
from ..src.char_detection import word_segmentation
from ..src.char_detection import update_traces

def test_find_char():

   img = cv2.imread('../fields/field_15.jpg', 1)

   dst = img_preprocess(img)

   bbox_list, traces_list = find_char(dst)
  
   bbox_list = word_segmentation(bbox_list, img)

   traces_list = update_traces(bbox_list, traces_list)

   assert len(bbox_list) == 5
