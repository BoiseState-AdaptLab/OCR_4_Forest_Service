# This file contains the test for the find_char functionality

import cv2
from ..src.char_detection import find_char
from ..src.char_detection import img_preprocess
from ..src.char_detection import word_segmentation
from ..src.char_detection import update_traces
from ..src.char_detection import single_chars

def test_find_char():

   img = cv2.imread('sawtooth.jpeg', 1)

   dst = img_preprocess(img)

   bbox_list, traces_list = find_char(dst)
  
   bbox_list = word_segmentation(bbox_list, img)

   traces_dict = update_traces(bbox_list, traces_list)

   list_single_char_img = single_chars(bbox_list, traces_dict)

   assert len(bbox_list) == 8
