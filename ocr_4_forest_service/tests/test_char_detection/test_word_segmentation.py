# This file contains the test for the find_char functionality

import cv2
from ...src.char_detection import trace
from ...src.char_detection import img_preprocess
from ...src.char_detection import word_segmentation
from ...src.char_detection import line_deletion
from ...src.char_detection import word_seg_2

def test_word_segmentation():

   img = cv2.imread('../../cropped_fields/KIND OF LIVESTOCK.jpg', 1)

   dst = img_preprocess(img)
   cv2.imshow(f"preprocess", dst)
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   con_img = line_deletion(dst)
   single_char_list = trace(con_img)
   for idx, char in enumerate(single_char_list):
         cv2.imshow(f"trace_{idx}", char)
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   word_seg_list = []
   word_seg = []
   for img in single_char_list:  
      sliced_images = word_segmentation(img, 'KIND OF LIVESTOCK')

      if sliced_images is None:
         # print("for one of them we get in here")
         break
      else:

         for img in sliced_images:
            # cv2.imshow('img', img[0])
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # cv2.imshow('Word segmentation 1', img[0])
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()s
            segmented_imgs = word_seg_2(img[0])
            print("segmented images", len(segmented_imgs))
         

            word_seg_list.extend(segmented_imgs)

      word_segmentation_list = [(x,'KIND OF LIVESTOCK') for x in word_seg_list]

   for idx, char in enumerate(word_seg):
       cv2.imshow(f"result_{idx}", char[0])

   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(word_seg) == 6




