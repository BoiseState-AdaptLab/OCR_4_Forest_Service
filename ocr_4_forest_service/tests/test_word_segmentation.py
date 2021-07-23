# This file contains the test for the find_char functionality

import cv2
from ..src.char_detection import img_preprocess
from ..src.char_detection import word_segmentation
#from ..src.char_detection import update_traces
from ..src.char_detection import trace

def test_find_char():

   img = cv2.imread('sawtooth.jpeg', 1)

   dst = img_preprocess(img)

   

   single_char_list = trace(dst)
  
   #bbox_list = word_segmentation(bbox_list, img)

   #traces_dict = update_traces(bbox_list, traces_list)

   #list_single_char_img = single_chars(bbox_list, traces_dict)

   assert len(single_char_list) == 8

def test_word_segmentation():
  img = cv2.imread("test_word_segmentation/one_output_from_trace().jpg")

  characters = word_segmentation(img)

  for idx, char in enumerate(characters):
    cv2.imshow(f"result_{idx}", char)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  assert len(characters) == 3
