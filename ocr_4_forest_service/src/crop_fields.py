# * Author: Floriana Ciaglia
# * Date: May 28th, 2021
# * File: crop_fields.py
# * Objective: This program takes in the input form and the json file with the
#              field coordinates as command line arguments, crops the fields
#              out of the form and returns them.
 
import json

"""
 Performs command line parsing and function calls
"""
def crop_fields(args, form):

    # read the input image in
    fields = read_inputs(args)

    # crop each field out of the 
    # form and return it
    return crop(form, fields)


"""
 Reads the input image in and loads the 
 json file 
"""
def read_inputs(args):
    
    # load the json file
    json_file = open(args["coord"])
    fields = json.load(json_file)

    return fields


"""
 Goes trough the coordinates, crops out the 
 portion of the image and returns it
"""
def crop(image, json_file):
    
    # the new cropped images are stored 
    # into a new list 
    field_imgs = []

    for field in json_file['fields']:
       
        x = (field['coord_pixel'][0])
        y = (field['coord_pixel'][1])
        w = field['width']
        h = field['height']

        # cropping the image
        cropped_img = image[y:y + h, x:x + w]

        # display the image to user
        if cropped_img is not None:
            
            field_imgs.append(cropped_img)
    
        else:
            print("Error: no image found [inside crop_fields/crop()].")
            exit(1)

    return field_imgs
        




