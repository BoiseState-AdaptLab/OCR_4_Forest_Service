# This script preprocesses the single letter images from the Forest Service Form. 
# Author: Floriana Ciaglia
# Date: May 1st, 2021
import cv2
import numpy as np
from matplotlib import pyplot as plt
import json
import os
from os import path 
from PIL import Image

def main():
  #read data from JSON file
  f = open("fields.json")
  fields = json.load(f)
  max_x = 0
  max_y = 0
  min_x = 10000
  min_y = 10000

  #if it doesn't exists already, create the 
  # folder where the preprocessed images will go
  if not os.path.exists('preprocessed'):
    os.makedirs('preprocessed')

  directory = '/Users/florianaciaglia/Google Drive/AdaptLab/forestService/OCR_4_Forest_Service/char_detection/output'

  for image in os.listdir(directory):
    #print("####### image")
    #set up the right string for the path 
    path = "output/" + image
    # read in the image in gray scale
    img = cv2.imread(path, 0) 
    if img is None:
      print(path)
      exit(1)

   
    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    #cv2.imshow("Blurred", blurred)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
  
    con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
    dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)
    #cv2.imshow("dst", dst)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
  
    #iterate through the pixels in dst
    # end_path = "preprocessed/" + image
    # cv2.imwrite(end_path, dst)

    # we need to save the image using 
    # the pillow library to iterate through
    # its pixels
    #print("shape ",dst.shape)
    im = Image.fromarray(dst)
    pixels = im.load() # create the pixel map


    #counter = 0
    # print("max x: ", im.size[0])
    # print("max y: ", im.size[1])
    #pixels[0,0] = (0, 255, 0)
    #im.show()
  
    for x in range(im.size[0]): # for every pixel:
      for y in range(im.size[1]):
        #print("in for loop")
        #if the pixel is not black
        if pixels[x,y] == (0, 0, 0):
          #print("in if statme")
          continue

        else: #we found the first non-black pixel
          #print("first found: ", x, y)
          #print('in else')
          pixels[x,y] = (0, 255, 0)
          #print("calling func")
          max_x, max_y, min_x, min_y = check_coord(x, y, max_x, min_x, max_y, min_y)
          # print("## max x: ", max_x)
          # print("## max y: ", max_y)
          # print("## min x: ", min_x)
          # print("## min y: ", min_y)

          # checking the width of character: right direction --> 
          temp = x
          
          while pixels[temp,y] != (0, 0, 0) and temp < im.size[0]-1:
            pixels[temp,y] = (0, temp, 0)
            # print(temp)
            # print(y)
            temp = temp+1
            #im.show()
            #counter = counter +1
          
          #pixels[temp,y] = (0, 255, 0)
          #print("calling func")
          max_x, max_y, min_x, min_y = check_coord(temp, y, max_x, min_x, max_y, min_y)
          # print("## max x: ", max_x)
          # print("## max y: ", max_y)
          # print("## min x: ", min_x)
          # print("## min y: ", min_y)
          #break
          
        #im.show()
          
        #break
      #break  
    #break 
            
      #break
  print("max x: ", max_x)
  print("max y: ", max_y)
  print("min x: ", min_x)
  print("min y: ", min_y)

  pixels[min_x, min_y] = (255, 0 , 0)
  pixels[max_x, min_y] = (255, 0 , 0)
  pixels[min_x, max_y] = (255, 0 , 0)
  pixels[max_x, max_y] = (255, 0 , 0)


# #show image
  im.show()

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
  # print("IN: max x: ", max_x)
  # print("IN: max y: ", max_y)
  # print("IN: min x: ", min_x)
  # print("IN: min y: ", min_y)
  return max_x, max_y, min_x, min_y

  

#main function
if __name__ == '__main__':
  main()
