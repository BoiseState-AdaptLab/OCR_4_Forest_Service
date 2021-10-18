# this file contains tests for the image enhancement
import cv2
import numpy as np
from ...src.char_detection import img_preprocess
from ...src.char_detection import line_deletion
from ...src.char_detection import trace

def test_preprocessing_techniques():
  
    img = cv2.imread('../../cropped_fields/KIND OF LIVESTOCK.jpg', 1)

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


    global_thresh = img_preprocess(img)

    cv2.imshow(f'global thresh', global_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(global_thresh.shape)


    # Phase 1 - Image Enhancement
    local_thresh = img_enhancement(img)

    cv2.imshow(f'local thresh', local_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(global_thresh.shape)


    cleaned_img = line_deletion(global_thresh)
    
    cv2.imshow(f'cleaned_img', cleaned_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    img_list = trace(cleaned_img)
    print(img_list)
    
    assert img == 1

    
def img_enhancement(img):
    print("inside enhancement")
    # perform the image preprocessing stepss
    # 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.THRESH_BINARY_INV+

    global_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 111, 0)
    cv2.imshow(f'thresholf', global_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
    con_img = cv2.cvtColor(global_thresh, cv2.COLOR_GRAY2BGR)
 
    return con_img


# def edge_connection():


def noise_reduction(img):
    
    return cv2.bilateralFilter(img,9,75,75)


