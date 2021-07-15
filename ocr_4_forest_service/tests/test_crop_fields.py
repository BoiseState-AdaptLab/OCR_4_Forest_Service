# This file contains the test function for the crop field functionality. 

from ..src.crop_fields import crop
from ..src.crop_fields import output_dir
import cv2
import json
import os

def test_cropFields():
    DIR = 'fields/'
    output_dir()

    # read in imputs
    image = cv2.imread("../inputs/template1.jpg")
    json_file = open("../inputs/all_fields_conservative.json")
    fields = json.load(json_file)

    # cropping function
    crop(image, fields)

    # we need to assert that the directory
    # of images that the output_dir function  
    # gets filled with the right amout of 
    # images by the crop function. 

    i = 0
 
    for image in os.listdir(DIR):
        i = i + 1

    assert i == 16 
