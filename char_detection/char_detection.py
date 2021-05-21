# Author: Floriana Ciaglia
# Date: May 14th, 2021

# This program attempts to create a bounding box around a discrete letter by:
#       - take a field image as an input
#       - iterate through each pixel in the image
#       - keep track of max x, max y, min x, min y

import cv2
import json
import shutil
import os
import os.path
from os import path
from PIL import Image
from queue import LifoQueue


def main():
    img_preprocess()
    # create_json(json_data)
  

#  This function opens an image and detects
#  each character in it
def img_preprocess():
    #read data from JSON file
    f = open("fields.json")
    fields = json.load(f)
    json_dict = {}  
    
    directory = '/Users/florianaciaglia/Google Drive/AdaptLab/forestService/OCR_4_Forest_Service/char_detection/output'

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("char_bbox.json"):
        file = open("char_bbox.json","r+")
        file.truncate(0)
        file.close()

    #for each image in the output directory:
    for image in os.listdir(directory):
        # print("We are processing ", image)
        #set up the right string for the path 
        path = "output/" + image

        # read in the image in gray scale
        img = cv2.imread(path, 0) 
        if img is None:
            print(path)
            exit(1)
        
        #perform the image preprocessing stepss
        blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
        con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        # print("we are still in preproc with ", image)
        json_data = find_char(dst, image, json_dict)
        create_json(json_data)

    # return dst, image, json_dict


def find_char(dst, img, json_dict):
    # print("we are in find char with ", img)
    #  max_x, max_y, min_x, min_y 
    max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
    active = False
    im = Image.fromarray(dst)
    pixels = im.load()
    json_dict.clear()
    json_list = []
    x = 0
    counter = 0
    
  
    #iterate through the pixels in dst
    while (x < im.size[0]): # for every pixel:
        y = 0
      
        while (y < im.size[1]):
          
            if pixels[x,y] != (0, 0, 0):
                
                max_x, min_x, max_y,  min_y = explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y)
              
                if valid_area(max_x, max_y, min_x, min_y):
                    pixels[min_x, min_y] = (255, 0 , 0)
                    pixels[max_x, min_y] = (255, 0 , 0)
                    pixels[min_x, max_y] = (255, 0 , 0)
                    pixels[max_x, max_y] = (255, 0 , 0)

                    counter = counter + 1
                    # name = name + str(counter)
                    json_list.append({'x': min_x, 
                                    'y': min_y, 
                                    'w': max_x-min_x,
                                    'h': max_y-min_y})
                # print("print list: ", json_list)
                # print("json dict: ", json_coor)
                y = 0

                x = max_x + 2
                if x > im.size[0]-1:
                    y = im.size[1]
                max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
                # print("before the else: ", x, y)

            else:
                y = y + 2
        
        x = x + 2
    
    #All the characters have been identified
    im.show()
    # print("json list: ", json_list)
    if valid_area(max_x, max_y, min_x, min_y):
        json_dict[img] = json_list
    # print("json_dict: ", json_dict)
    return json_dict
 

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

def create_json(json_data):
    # store the data into a new json file
    with open('char_bbox.json', 'a') as outfile:
        json.dump(json_data, outfile)
    # with open("cropped.json", "r+") as file:
    #     data = json.load(file)
    #     data.update(json_data)
    #     file.seek(0)
    #     json.dump(data, file)
    

    
def x_in_bound(x, im):
    if x >= 0 and x <= im.size[0]-1:
        return True
    else:
        return False

def y_in_bound(y, im):
  
    if y >= 0 and y <= im.size[1]-1:
        return True
    else:
        return False

def explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y):
    # Initializing a values
    stack = []
    jump_size = 1

    stack.append((x,y))
    

    # while the stack holds tuples
    while len(stack) != 0:
        # print("Stack at beginning : ", stack)

        pair = stack.pop(len(stack)-1)
        # print("pair: ", pair[0], pair[1])

        # if the pixel is already green, we have already visited it
        if x_in_bound(pair[0], im) and y_in_bound(pair[1], im) and pixels[pair[0], pair[1]] != (0, 255, 0):

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




def look(x, y, im, pixels):

    retVal = False
    # check if x and y are in bound
    if x_in_bound(x, im) and y_in_bound(y, im):
        if pixels[x, y] != (0, 0, 0):
            retVal = True

    return retVal


def look_left(x, y, im, pixels, jump_size):
    
    retVal = False
     
    if x_in_bound(x, im) and y_in_bound(y, im):
        
        if x > jump_size:
            if pixels[x-jump_size, y] != (0, 0, 0):
                retVal = True
        elif x <= jump_size and x >= 0:       
            if pixels[x-1, y] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
                retVal = True

    return retVal

def look_down(x, y, im, pixels, jump_size):
    
    
    retVal = False
    if x_in_bound(x, im) and y_in_bound(y, im):
        if y < im.size[1]-jump_size:
            if pixels[x, y+jump_size] != (0, 0, 0):
                retVal = True
        elif y > im.size[1]-jump_size and y < im.size[1]-1:       
            if pixels[x, y+1] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
                retVal = True

    return retVal


def look_up(x, y, im, pixels, jump_size):
    
    retVal = False

    if x_in_bound(x, im) and y_in_bound(y, im):
        if y > jump_size:
            if pixels[x, y-jump_size] != (0, 0, 0):
                retVal = True
        elif y <= jump_size and y >= 0:       
            if pixels[x, y-1] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
                retVal = True

    # print("retVal: " , retVal)
    return retVal


def check_coord(x, y, max_x, min_x, max_y, min_y):
  if x > max_x:
    max_x = x
  
  if x < min_x:
    min_x = x
    
  if y > max_y:
    max_y = y
   
  if y < min_y:
    min_y = y
#   print("inside check coord: ", max_x, max_y, min_x, min_y)
  return max_x, min_x, max_y,  min_y



# main function
if __name__ == '__main__':
    main()
