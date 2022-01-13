# this file contains the tests for the image preprocessing function inside the character
# detection section of the code

import cv2
from ...src.char_detection import img_preprocess

def test_img_preprocess():

    img = cv2.imread('input_imgs/field_4.jpg', 1)

    dst = img_preprocess(img)

    cv2.imshow('preprocessed img', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    assert img.shape == dst.shape

