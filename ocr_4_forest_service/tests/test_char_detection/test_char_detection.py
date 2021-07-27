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


def test_char_detection_0():

   img = cv2.imread('input_imgs/tcd_field_0.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 2
   

def test_char_detection_1():

   img = cv2.imread('input_imgs/tcd_field_1.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 8


def test_char_detection_2():

   img = cv2.imread('input_imgs/tcd_field_2.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 9


def test_char_detection_3():

   img = cv2.imread('input_imgs/tcd_field_3.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 6


def test_char_detection_4():

   img = cv2.imread('input_imgs/tcd_field_4.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 2


def test_char_detection_5():

   img = cv2.imread('input_imgs/tcd_field_5.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 2


def test_char_detection_6():

   img = cv2.imread('input_imgs/tcd_field_6.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 4


def test_char_detection_7():

   img = cv2.imread('input_imgs/tcd_field_7.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 2


def test_char_detection_8():

   img = cv2.imread('input_imgs/tcd_field_8.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 8


def test_char_detection_9():

   img = cv2.imread('input_imgs/tcd_field_9.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 9

def test_char_detection_10():

   img = cv2.imread('input_imgs/tcd_field_10.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 7


def test_char_detection_11():

   img = cv2.imread('input_imgs/tcd_field_11.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 13


def test_char_detection_12():

   img = cv2.imread('input_imgs/tcd_field_12.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 7


def test_char_detection_13():

   img = cv2.imread('input_imgs/tcd_field_13.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 6


def test_char_detection_14():

   img = cv2.imread('input_imgs/tcd_field_14.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 2

def test_char_detection_15():

   img = cv2.imread('input_imgs/tcd_field_15.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 6

def test_char_detection_16():

   img = cv2.imread('input_imgs/tcd_field_16.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 5


def test_char_detection_17():

   img = cv2.imread('input_imgs/tcd_field_17.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 9


def test_char_detection_18():

   img = cv2.imread('input_imgs/tcd_field_18.jpg')
   field_chars = char_detection(img)

   for idx, img in enumerate(field_chars):
      cv2.imshow(f'img_{idx}', img)
 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   assert len(field_chars) == 4