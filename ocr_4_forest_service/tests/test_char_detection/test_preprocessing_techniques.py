# this file contains tests for the image enhancement
import cv2
import numpy as np
from ...src.char_detection import img_preprocess
from ...src.char_detection import line_deletion
from ...src.char_detection import trace

def test_preprocessing_techniques():
  
    img = cv2.imread('../../cropped_fields/TRANSECT NO..jpg', 1)
    if img is None:
        print("image is None")
        exit()
    cv2.imshow(f'original', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(global_thresh.shape)
    

    if img is None:
        print("Error reading the image")
        exit(1)

    # Phase 1 - Image Enhancement
    global_thresh = img_preprocess(img)

    cv2.imshow(f'global thresh', global_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(global_thresh.shape)


    cleaned_img = line_deletion(global_thresh)
    
    cv2.imshow(f'cleaned_img', cleaned_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    img_list = trace(cleaned_img)

    
    assert img == 1

    
def img_enhancement(img):
    print("inside enhancement")
    # perform the image preprocessing stepss
    # 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, global_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
   
    con_img = cv2.cvtColor(global_thresh, cv2.COLOR_GRAY2BGR)
 
    return con_img


# def edge_connection():


def noise_reduction(img):
    
    return cv2.bilateralFilter(img,9,75,75)


