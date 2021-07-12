# This script preprocesses the single letter images from the Forest Service Form. 
# Author: Floriana Ciaglia
# Date: May 1st, 2021
import cv2
import numpy as np
from matplotlib import pyplot as plt
import json
import os
from os import path 

def main():
  #read data from JSON file
  f = open("high_res.json")

  #returns JSON object as a dictionary
  data = json.load(f)

  # create a dictionary to map each letter/digit to a number 
  class_dict = {}
  data_dict = {}
  counter = 0

  # these are all the possible valid classifications
  classifications = ['0', '1','2','3','4','5','6','7','8','9', 'A','B','C','D','E',
            'F','G','H','I','J','K','L','M','N','O', 'P','Q','R','S','T',
            'U','V','W','X','Y', 'Z', 'a','b','d','e','f','g','h','n','q','r','t']

  # Iterating through the json
  # list and populating the dict
  for entry in data['character']:
    data_dict[entry['img']] = entry['class']
    

  for clas in classifications:
    class_dict[clas]=counter
    counter = counter + 1

  names = [name for name in data_dict]
  labels = [label for label in class_dict]

  #if it doesn't exists already, create the 
  # folder where the preprocessed images will go
  if not os.path.exists('preprocessed'):
    os.makedirs('preprocessed')

  for image in names:
    #set up the right string for the path 
    path = "output/" + image
    # read in the image in gray scale
    img = cv2.imread(path, 0) 
    if img is None:
      print(path)
      exit(1)
    #perform Gaussinan blur on the image
    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
   
    #create a histogram on the images colors
    hist = plt.hist(blurred.ravel(), 256, [0,256])
   
    # THIS SECTION MIGHT NOT BE NECESSARY IN THE FUTURE. 
    ########################################################
    # 25% of 28x28 pixels (784) is 196 pixels.
    # iterate through the first 196 pixels and
    # add up their x values.
    x_value = {}
    counter = 0
    add = 0
    
    # hist is a tuple. We are only
    # interested in the first field
    # which contains the x values
    for item in hist[0]:
      x_value[counter] = item
      counter = counter + 1
    
    # turn the dict to a list to iterate through it
    x_list = list(x_value.values())

    for i in x_list:
      #196 is the 25% mark
      if add < 196:
        add = add + i
      else:
        # we want to know at what 
        # position we reached 25%
        adds = i
        break

    # create and populate the list of values
    # that match a specific x. 
    pos = []
    for i, x in x_value.items():
      if x == adds:
        pos.append(i)
 
    thresh_num = int(max(pos))
    # taking the average of the values in pos[]
    # to estimate a good thresh value. 
    #thresh_num = 0
    #for i in pos:
    #    thresh_num = thresh_num + i
    
    #thresh_num = int(thresh_num / len(pos))
    ######################################################
   
#    ret, thresh = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow("thresholded", thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

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
  
    end_path = "preprocessed/" + image
    cv2.imwrite(end_path, dst)

#main function
if __name__ == '__main__':
  main()
