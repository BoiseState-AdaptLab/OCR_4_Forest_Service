# This file contains the test for the find_char functionality

import cv2
from ...src.char_detection import trace
from ...src.char_detection import img_preprocess
from ...src.char_detection import word_segmentation

def test_word_segmentation():

   img = cv2.imread('../../cropped_fields/PLOT INTERVAL.jpg', 1)

   dst = img_preprocess(img)

   single_char_list = trace(dst)
#   for idx, char in enumerate(single_char_list):
#       cv2.imshow(f"result_{idx}", char)
#   cv2.waitKey(0)
#   cv2.destroyAllWindows()
   word_seg = []
   for img in single_char_list:  
       characters = word_segmentation(img)

       if type(characters) == list:
          # if the output is a list, we extend the list
          word_seg.extend(characters)
       else:
           # if it's a signle image, we append it to the list
           word_seg.append(characters)

   for idx, char in enumerate(word_seg):
       cv2.imshow(f"result_{idx}", char)

   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(word_seg) == 2





