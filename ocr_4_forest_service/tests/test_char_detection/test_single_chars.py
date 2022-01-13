# This file contains the tests for the single_chars() function

import cv2
from ...src.char_detection import find_char
from ...src.char_detection import single_chars
from ...src.char_detection import img_preprocess

def test_find_char():

   img = cv2.imread('input_imgs/test-word.jpeg', 1)

   dst = img_preprocess(img)

   bbox_list, traces_list = find_char(dst)

   list_images = single_chars(bbox_list, traces_list)

   for idx, img in enumerate(list_images):
        cv2.imshow(f'img_{idx}', img)

   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(list_images) == 7
