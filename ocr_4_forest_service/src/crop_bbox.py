#   Author: Floriana Ciaglia
#   Date: May 24th, 2021
#   Description: This file contains functions that open the JSON file and crop 
#   the bounding boxes out of the form.

import cv2
import os
import json
import shutil
from PIL import Image


def crop_bbox(args):

    # open json file bbox_coord.json with bbox coordinates
    fields = open_json(args)

    return crop(fields, args['input'])
    
    

"""
Load the data from the bbox coord file
"""
def open_json(args):

    json_file = open(args["coord"])
 
    fields = json.load(json_file)
    return fields
    


def crop(json, image):

    single_chars = []

    # open form as an image
    img = cv2.imread(image)

    for char in json['character']:
       
        x = int(char['x'])
        y = int(char['y'])
        w = int(char['w'])
        h = int(char['h'])
        classi = str(char['class'])

        # cropping the image
        cropped_img = img[y:y + h, x:x + w]
        
        if cropped_img is not None:
        
            single_chars.append((cropped_img, classi))

        else:
            print("Error: no image has been read.")


    return single_chars
 
        




