# * Author: Floriana Ciaglia
# * Date: May 28th, 2021
# * File: crop_fields.py
# * Objective: First step in the base pipeline. This program takes in the input form and the 
#              json file with the field coordinates as command line arguments, crops the fields
#              out of the form and stores them as new images in a newly generated fields/ directory.
 
import cv2
import os
import json
import shutil


"""
 Performs command line parsing and function calls
"""
def crop_fields(args):

    # read the input image in
    form, fields = read_inputs(args)

    # create the output directory 
    # to store the images
    output_dir()

    # crop each field out of the 
    # form and stores them in fields/
    crop(form, fields)



    
"""
 if the output dir already exists, it gets
 cleaned up. Otherwise, it gets created 
"""
def output_dir():
    # if it already exists, clean it
    if os.path.exists('fields'):
        try:
            shutil.rmtree('fields')
        except:
            print("Error: couldn't clean the fields/ directory")
    # else, create it
    if not os.path.exists('fields'):
        os.makedirs('fields')


"""
 Reads the input image in and loads the 
 json file 
"""
def read_inputs(args):
    # load input image
    form = cv2.imread("alignedImage.jpg")
    
    # load the json file
    json_file = open(args["coord"])
    fields = json.load(json_file)

    return form, fields


"""
 Goes trough the coordinates, crops out the 
 portion of the image and returns it
"""
def crop(image, json_file):
    i = 0

    for field in json_file['fields']:
       
        x = (field['coord_pixel'][0])
        y = (field['coord_pixel'][1])
        w = field['width']
        h = field['height']

        # cropping the image
        cropped_img = image[y:y + h, x:x + w]

        # display the image to user
        if cropped_img is not None:
            
            # cv2.imshow(window_name, cropped_img)
            cv2.imwrite('fields/field_{num}.jpg'.format(num = i), cropped_img)
    

        else:
            print("Error: no image has been read.")

        i = i + 1 




