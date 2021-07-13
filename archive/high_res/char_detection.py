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
from PIL import Image
from queue import LifoQueue

def main():
    preprocessed_img = img_preprocess()
    find_char(preprocessed_img)
  

#  This function opens an image and detects
#  each character in it
def img_preprocess():
    #read data from JSON file
    f = open("fields.json")
    fields = json.load(f)

    #if it doesn't exists already, create the 
    # folder where the preprocessed images will go
    if not os.path.exists('preprocessed'):
        os.makedirs('preprocessed')

    directory = '/Users/florianaciaglia/Google Drive/AdaptLab/forestService/OCR_4_Forest_Service/char_detection/output'

    #for each image in the output directory:
    for image in os.listdir(directory):
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
        blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
        con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)

        print("## Finished image preprocessing")
        cv2.imshow('dst', dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return dst


def find_char(dst):
    print("Inside of find_char()")
    active = False
    im = Image.fromarray(dst)
    pixels = im.load()

    #iterate through the pixels in dst
    for x in range(im.size[0]): # for every pixel:
        for y in range(im.size[1]):
            
            #if the pixel is black
            if pixels[x,y] == (0, 0, 0):
                
                # do nothing
                continue

            else: #we found the first non-black pixel
                active = True
                print("Before call to explore_active()")
                max_x, max_y, min_x, min_y = explore_active(x, y, pixels)
                 #  marking the corner of each bbox
                pixels[min_x, min_y] = (255, 0 , 0)
                pixels[max_x, min_y] = (255, 0 , 0)
                pixels[min_x, max_y] = (255, 0 , 0)
                pixels[max_x, max_y] = (255, 0 , 0)
                break

        x = max_x + 2
        y = 0

    im.show()



def explore_active(x, y, pixels):
    print("Inside explore_active()")
    # Initializing a values
    stack = []
    max_x = 0
    max_y = 0
    min_x = 10000
    min_y = 10000

    stack.append((x,y))

    print("stack: ", stack)

    # while the stack holds tuples
    while len(stack) != 0:
        for pair in stack:
            if look_right(pair[0], pair[1], pixels):
                stack.append((pair[0]+3,pair[1]))
                check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            if look_down(pair[0], pair[1], pixels):
                stack.append((pair[0],pair[1]+3))
                check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            if look_left(pair[0], pair[1], pixels):
                stack.append((pair[0]-3,pair[1]))
                check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            if look_up(pair[0], pair[1], pixels):
                stack.append((pair[0],pair[1]-3))
                check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            stack.remove(pair)

   

    return max_x, max_y, min_x, min_y

def look_right(x, y, pixels):
    if pixels[x+3, y] != (0, 0, 0):
        return True
    else:
        return False

def look_left(x, y, pixels):
    if pixels[x-3, y] != (0, 0, 0):
        return True
    else:
        return False

def look_down(x, y, pixels):
    if pixels[x, y+3] != (0, 0, 0):
        return True
    else:
        return False

def look_up(x, y, pixels):
    if pixels[x, y-3] != (0, 0, 0):
        return True
    else:
        return False


def check_coord(x, y, max_x, min_x, max_y, min_y):
  if x > max_x:
    # print("x:" , x)
    # print("max_x: ", max_x)
    max_x = x
    # print("max_x: ", max_x)
  if x < min_x:
    # print("x:" , x)
    # print("min_x: ", min_x)
    min_x = x
    # print("min_x: ", min_x)
  if y > max_y:
    # print("y: ", y)
    # print("max_y: ", max_y)
    max_y = y
    # print("max_y: ", max_y)
  if y < min_y:
    # print("y: ", y)
    # print("min_y: ", min_y)
    min_y = y
  #   print("min_y: ", min_y)
  #   print(" ")
  print("IN: max x: ", max_x)
  print("IN: max y: ", max_y)
  print("IN: min x: ", min_x)
  print("IN: min y: ", min_y)
  return max_x, max_y, min_x, min_y



# main function
if __name__ == '__main__':
    main()