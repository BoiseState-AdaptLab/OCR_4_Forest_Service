# This file contains tests character detection functionalities on single fields

from ..src.char_detection import find_char
from ..src.char_detection import create_json
from ..src.char_detection import word_segmentation
from ..src.crop_bbox import output_dir
from ..src.crop_bbox import crop
import cv2
import os
import json


def test_field_0():
    DIR = 'fields/'
    image = 'field_0.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_0_coord.json"):
        file = open("field_0_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(dst, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_0_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_0'):
        try:
            shutil.rmtree('field_0')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_0'):
        os.makedirs('field_0')
    

    json_file = open('field_0_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_0/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_0/'):
        count = count + 1
   
    assert count == 3



 
