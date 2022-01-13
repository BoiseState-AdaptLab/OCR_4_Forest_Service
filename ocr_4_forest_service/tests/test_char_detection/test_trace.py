# this file contains tests for the character tracing feature
import cv2
from ...src.char_detection import trace
from ...src.char_detection import line_deletion
from ...src.char_detection import img_preprocess

def test_tracing():
  
    img = cv2.imread('../../cropped_fields/FOREST.jpg', 1)

    if img is None:
        print("Error reading the image")
        exit(1)

    dst = img_preprocess(img)
    cv2.imshow(f'img_preprocessing', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    con_img = line_deletion(dst)
    cv2.imshow(f'line_deletion', con_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img_list = trace(con_img) 
    
    for idx, img in enumerate(img_list):
        cv2.imshow(f'img_{idx}', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    assert len(img_list) == 8

