# this file contains tests for the character tracing feature
import cv2
from ...src.char_detection import trace
from ...src.char_detection import img_preprocess

def test_tracing():
  
    img = cv2.imread('input_imgs/test-word.jpeg', 1)

    if img is None:
        print("Error reading the image")
        exit(1)

    dst = img_preprocess(img)

    img_list = trace(dst) 
    
    for idx, img in enumerate(img_list):
        cv2.imshow(f'img_{idx}', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    assert len(img_list) == 7










   


    
