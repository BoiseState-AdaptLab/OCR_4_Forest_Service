# This file contains tests for the whole character detection pipeline
import cv2
from ...src.char_detection import char_detection

def test_char_detection():

   img = cv2.imread('input_imgs/field_img.png')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 4


   

