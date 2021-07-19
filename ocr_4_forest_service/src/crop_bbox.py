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
    # clean the directory from previous data
    # or create it
    output_dir()

    # open json file bbox_coord.json with bbox coordinates
    fields = open_json(args)

    if args['t'] is True:
        # print(args['input'])
        # crop the bbox out of the form
        test_crop(fields, args['input'])
    else:
        # iterate through fields and find the bboxes
        crop(fields)
        # exit()
    

   

"""
Load the data from the bbox coord file
"""
def open_json(args):

    if args['t'] is True:
        # read the manually generaterd JSON file
        json_file = open(args["coord"])
    else:   
        # load the json file
        json_file = open('bbox_coord.json')

    fields = json.load(json_file)
    return fields
    


"""
 if the output dir already exists, it gets
 cleaned up. Otherwise, it gets created 
"""
def output_dir():
    # if it already exists, clean it
    if os.path.exists('single_chars'):
        try:
            shutil.rmtree('single_chars')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('single_chars'):
        os.makedirs('single_chars')


"""
Iterates through fields and marks the min and max of bbox
around a character
"""
def crop(fields):
    DIR = 'fields/'
    i = 0

    for dict in fields:
        # print("dict: ", dict)
        # we only get the key
        new_d = [str(key) for key in dict.keys()]
        print("name of field: ", new_d[0])
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)
        
        for boxes in dict.values():
            # print(len(boxes))
            for box in boxes:
                
                name = box['box']
                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                tracing_image(cropped_img, new_d, name, x, y)
            
                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('single_chars/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 


def tracing_image(cropped_img, field_name, box_name, x_coord, y_coord):
    # print("x and y from bbox: ", x_coord, y_coord)

    cv2.imwrite('cropped.jpg', cropped_img)

    # read the image using pillow library
    im = Image.open('cropped.jpg')
    print(im.size)
    # make a copy of the image
    trace_image = im.copy()
    print(trace_image.size)
    #coloring the image with the background color
    width, height = trace_image.size
    # print(width)
    # print(height)
    for x in range(width):
        for y in range(height):
            trace_image.putpixel((x,y), (130,181,169,255)) # this is the form's background color

    # Read the json file with the tracings
    json_traces = open('tracing_list.json')
    traces = json.load(json_traces)

    for field in traces:

        for f_name, tracings in field.items():

            if f_name == field_name[0]:

                for char in tracings:
                    # print(type(box))
                    # print("this is the char name: ", name)
                    if char[0] == box_name:
                        # print(type(char))
                        for tuple in (number+1 for number in range(len(char)-1)):
                            # print("tracing coord: ", char[tuple][0], char[tuple][1])
                            tuple = (char[tuple][0]-x_coord, char[tuple][1]-y_coord)
                            # print("result", tuple)
                            pix = im.getpixel(tuple)
                            # print(pix)
                            trace_image.putpixel(tuple, pix)

                        trace_image.show()
                        # exit()
                                   


def test_crop(json, image):

    i = 0
    # open form as an image
    img = cv2.imread(image)

    for char in json['character']:
       
        x = int(char['x'])
        y = int(char['y'])
        w = int(char['w'])
        h = int(char['h'])

        # cropping the image
        cropped_img = img[y:y + h, x:x + w]
        
     
        if cropped_img is not None:
         
            cv2.imwrite('single_chars/field_{num}.jpg'.format(num = i), cropped_img)
    

        else:
            print("Error: no image has been read.")


        i = i + 1 
 
        




