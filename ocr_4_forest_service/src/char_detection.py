# Author: Floriana Ciaglia
# Date: May 14th, 2021

# This program creates a bounding box around a discrete letter by:
#       - take a field image as an input
#       - iterate through each pixel in the image
#       - keep track of max x, max y, min x, min y

# Generates a JSON file called bbox_coord.json the coordinates of each detected bounding box

import cv2
import json
import os
import os.path
from os import path
from PIL import Image
from queue import LifoQueue

"""
Definition of the main fuction
"""
def char_detection():
    img_preprocess()
    
  

"""
Performs the image preprocessing on the field image 
before bounding boxes identification
"""
def img_preprocess():
    DIR = "fields/"

    # this is the list where 
    # each images data is stored 
    list_of_dict = []

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("bbox_coord.json"):
        file = open("bbox_coord.json","r+")
        file.truncate(0)
        file.close()
  
    
    #for each image in the output directory:
    for image in os.listdir(DIR):
        json_dict = {} 
        #set up the right string for the path 
        path = DIR + image
        
        # read in the image in gray scale
        img = cv2.imread(path, 0) 
        if img is None:
            print(path)
            exit(1)
        
        #perform the image preprocessing stepss
        blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
      
        con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
        json_data = find_char(dst, image, json_dict)
        list_of_dict.append(json_data)

    create_json(list_of_dict)
    


"""
Iterates through the image until it finds a character. 
It explores the character to find its max_x, min_x, max_y, min_y
@return dictionary of data to populate the json file
"""
def find_char(dst, img, json_dict):
     
    max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
    json_list = []
    x = 0

    # Open the image using the PIL library
    im = Image.fromarray(dst)
    pixels = im.load()
    
    # clean the dictionary out 
    # before adding a new image
    json_dict.clear()

    #iterate through the pixels in dst
    while (x < im.size[0]): # for every pixel:
        y = 0
      
        while (y < im.size[1]):
          
            if pixels[x,y] != (0, 0, 0):
                
                max_x, min_x, max_y,  min_y = explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y)
              
                # if the area is big enough we identify it as a character
                if valid_area(max_x, max_y, min_x, min_y):
                    pixels[min_x, min_y] = (255, 0 , 0)
                    pixels[max_x, min_y] = (255, 0 , 0)
                    pixels[min_x, max_y] = (255, 0 , 0)
                    pixels[max_x, max_y] = (255, 0 , 0)

                    
                    json_list.append({'x': min_x, 
                                    'y': min_y, 
                                    'w': max_x-min_x,
                                    'h': max_y-min_y})
        
                y = 0

                x = max_x + 2
                if x > im.size[0]-1:
                    y = im.size[1]
                max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
               

            else:
                y = y + 2
        
        x = x + 2
    
    #All the characters have been identified
  
    if valid_area(max_x, max_y, min_x, min_y):
        json_dict[img] = json_list
    
    return json_dict
 

"""
Accepts only the areas that are bigger than 100
@return boolean
"""
def valid_area(max_x, max_y, min_x, min_y):
    # calculate the area of the bbox to 
    # minimize noise
    width = max_x - min_x
    height = max_y - min_y
    area = width * height
    if area > 100:
        return True
    else:
        return False

 
"""
Creates the json file with the bbox coordinates
"""
def create_json(list_of_dict):
    
    # store the data into a new json file
    with open("bbox_coord.json", 'a') as outfile: 
        json.dump(list_of_dict, outfile)
    


"""
Checks the x axis boundary
@return boolean
"""    
def x_in_bound(x, im):
    if x >= 0 and x <= im.size[0]-1:
        return True
    else:
        return False

"""
Checks the y axis boundary
@return boolean
"""
def y_in_bound(y, im):
  
    if y >= 0 and y <= im.size[1]-1:
        return True
    else:
        return False


"""
Loops through all the pixels in the stack and colors them green when visited
@return min and max coordinates
"""
def explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y):
    # Initializing a values
    stack = []
    jump_size = 1
    stack.append((x,y))
    
    # while the stack holds tuples
    while len(stack) != 0:

        # pop the first pair off the stack
        pair = stack.pop(len(stack)-1)

        # if the pixel is already green, we have already visited it
        if x_in_bound(pair[0], im) and y_in_bound(pair[1], im) and pixels[pair[0], pair[1]] != (0, 255, 0):

            # check and update the bbox coordinates
            max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            # check to the right
            if look(pair[0]+jump_size, pair[1], im, pixels):
                stack.append((pair[0]+jump_size,pair[1]))

            # check down-wards
            if look(pair[0], pair[1]+jump_size, im, pixels):
                stack.append((pair[0],pair[1]+jump_size))

            # check to the left 
            if look(pair[0]-jump_size, pair[1], im, pixels):
                stack.append((pair[0]-jump_size,pair[1])) 

            # check up-wards
            if look(pair[0], pair[1]-jump_size, im, pixels):
                stack.append((pair[0],pair[1]-jump_size)) 
            
            #turn the pixel green to sign it as visited
            pixels[pair[0], pair[1]] = (0, 255, 0)

    
    return max_x, min_x, max_y,  min_y


"""
Looks if the neighbor pixels is available
"""
def look(x, y, im, pixels):

    retVal = False
    # check if x and y are in bound
    if x_in_bound(x, im) and y_in_bound(y, im):
        if pixels[x, y] != (0, 0, 0):
            retVal = True

    return retVal


"""
Updates the max and min coordinates
"""
def check_coord(x, y, max_x, min_x, max_y, min_y):
  if x > max_x:
    max_x = x
  
  if x < min_x:
    min_x = x
    
  if y > max_y:
    max_y = y
   
  if y < min_y:
    min_y = y

  return max_x, min_x, max_y,  min_y


