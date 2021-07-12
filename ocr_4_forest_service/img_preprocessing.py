# Author: Floriana Ciaglia
# Date: May 1st, 2021
# This script preprocesses the single letter images from the Forest Service Form and create 
# the csv file that will work as input for the OCR model. 

import cv2
import numpy as np
from matplotlib import pyplot as plt
import json
import os
from os import path 
from PIL import Image
import csv

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

  # open and clean the cvs file up so
  # that is it ready for a fresh set of data points
  file = open("test_data.csv","w")
  file.truncate(0)
  file.close()

  #if it doesn't exists already, create the 
  # folder where the preprocessed images will go
  if not os.path.exists('preprocessed'):
    os.makedirs('preprocessed')

  location = 0
  for image in names:
    #set up the right string for the path 
    path = "single_chars/" + image
    # read in the image in gray scale
    img = cv2.imread(path, 0) 
    if img is None:
      print(path)
      exit(1)

    # blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    #cv2.imshow("Blurred", blurred)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
  
    con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
    dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)
    #cv2.imshow("dst", dst)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    resized = cv2.resize(dst, (28,28))

    end_path = "preprocessed/" + image
    cv2.imwrite(end_path, resized)

    # we need to save the image using 
    # the pillow library to iterate through
    # its pixels
    im = Image.fromarray(img)

    #At this point, the image is ready
    #list of RGB values for each pixel in the image
    pix = []
    
    #classification in number
    classi = data_dict[image]
    numeric_class = class_dict[classi]

    #the first column in the csv file is the classification
    pix.append(numeric_class)
    #pix.append(label_dict[labels[location]])
  

    #iterate through each pixel in the image and store its RBG value into a list
    for x in range(28):
        for y in range(28):
            rbg_val = im.getpixel((x,y))
            pix.append(rbg_val)
  
    with open('test_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(pix)
        file.close()
    location = location + 1

  
  # #iterate through each image in images/
  # for image in names:
  #   # read the image in
  #   my_path = "preprocessed/" + image
  #   original = cv2.imread(my_path,0)
  #   if original is None:
  #     print("Cannot find the image")
    
  #   # make sure it's the right shape
  #   img = cv2.resize(original, (28,28))

  #   # we need to save the image using 
  #   # the pillow library to iterate through
  #   # its pixels
  #   im = Image.fromarray(img)
  #   #new_name = "images/" + image
  #   #im.save(new_name, 'JPEG')
  #   #img = Image.open(new_name)
    
  #   #At this point, the image is ready
  #   #list of RGB values for each pixel in the image
  #   pix = []
  #   #classification in number
  #   classi = data_dict[image]
  #   numeric_class = class_dict[classi]

  #   #the first column in the csv file is the classification
  #   pix.append(numeric_class)
  #   #pix.append(label_dict[labels[location]])
  

  #   #iterate through each pixel in the image and store its RBG value into a list
  #   for x in range(28):
  #       for y in range(28):
  #           rbg_val = im.getpixel((x,y))
  #           pix.append(rbg_val)
  
  #   with open('test_data.csv', 'a', newline='') as file:
  #       writer = csv.writer(file)
  #       writer.writerow(pix)
  #       file.close()
  #   location = location + 1

#main function
if __name__ == '__main__':
  main()
