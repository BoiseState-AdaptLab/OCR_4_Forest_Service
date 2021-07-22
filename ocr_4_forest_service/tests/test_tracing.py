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



# @param: image object
# @return: list of image objects
# This function takes in an image 
# objects, performs character detection 
# on the image, saves the tracing and 
# creates the another image with the 
# trace of the letter.  
def trace(image):
    # this is the list where 
    # each images data is stored 
    list_of_dict = []
    list_of_tracings = []
 
    json_dict = {} 
    tracing_dict = {}

    # 1) We need to perform character 
    # detection on the field image
    # Char_detection contains: image preprocessing, 
    con_img = img_preprocess(image)

    json_data, tracing_data = find_char(con_img)

    # print("json_data", json_data)

    list_of_dict.append(json_data)
    
    list_of_tracings.append(tracing_data)
    list_images = []
   
    for field in list_of_dict:
        for box in field.items():
            for bbox in box[1]:
                box_name = bbox['box']
                x_coord = bbox['x']
                y_coord = bbox['y']
                width = bbox['w']
                height = bbox['h']
                for im in list_of_tracings:
                    for list in im.items():
                        for pix_list in list[1]:
                            #b_box is the list of pixels
                            b_name = pix_list[0]
                            if b_name == box_name:
                                new_image = create_img(pix_list, x_coord, y_coord, width, height)
                                list_images.append(new_image)
    return list_images



def create_img(pix_list, x_coord, y_coord, width, height):

    # print("x and y coords: ", x_coord, y_coord)
    new_image = np.zeros((width, height, 3), np.uint8)
    new_image[:] = (255, 255, 255)
 

    nI = len(pix_list)
    for pix in range(1, nI):
        # print(pix_list[pix])
        # # exit()
        # print("tracing coord: ", pix_list[pix][0], pix_list[pix][1])
    
        # tuple = (pix_list[pix][0]-x_coord, pix_list[pix][1]-y_coord)
        new_image[pix_list[pix][0]-x_coord, pix_list[pix][1]-y_coord] = [0, 0, 0]
        # image[pix_list[pix][0], pix_list[pix][1]] = [255, 255]
        # print("result", tuple)
        # print(im.size)
        # pix = im.getpixel(tuple)
        # # # print(pix)s
        # new_im.putpixel(tuple, pix)

    return new_image





def img_preprocess(img):
  
    #perform the image preprocessing steps
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    return con_img
   


    