# this file contains tests for the character tracing feature
import cv2
import numpy as np
from PIL import Image
from ..src.char_detection import find_char

def test_tracing():
  
    img = cv2.imread('../inputs/test-word.jpeg', 0)

    if img is None:
        print("Error reading the image")
        exit(1)

    img_list = trace(img) 

    i = 0
    for img in img_list:
        cv2.imwrite('box_{num}.jpg'.format(num = i), img)
        i += 1
    
    assert len(img_list) == 9










   


    