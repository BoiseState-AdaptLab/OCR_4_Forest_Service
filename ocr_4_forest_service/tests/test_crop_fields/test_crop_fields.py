# This file contains the test function for the crop field functionality. 

from ...src.crop_fields import crop
from ...src.form_alignment import align_images
import cv2
import json

def test_cropFields():

    max_features = 1000
    keep_percent = 0.2

    # read in imputs
    form = cv2.imread('../../inputs/forms/site_an_sum_25.jpeg')
    temp = cv2.imread('../../inputs/forms/template2.jpg')

    json_file = open("../../inputs/jsons/template2_field_coord.json")
    fields = json.load(json_file)

    aligned = align_images(form, temp, max_features, keep_percent)
    # cropping function
    field_imgs = crop(aligned, fields)

    i = 0
 
    for image in field_imgs:
        i = i + 1

    assert i == 16 
