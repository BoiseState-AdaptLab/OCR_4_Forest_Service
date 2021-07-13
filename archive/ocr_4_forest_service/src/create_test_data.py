## Author: Floriana Ciaglia
## Date: March 19th, 2021
## File: This driver iterates through our testing images and generates
## a csv file with the RGB value of each pixel for each image

import cv2 as cv
from matplotlib import pyplot as plt
import csv
import PIL
from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter
from PIL import ImageEnhance
from IPython.display import display
import os
from os import path
import json

def main():
    
    digits = ['0', '1','2','3','4','5','6','7','8','9', 'A','B','C','D','E',
                'F','G','H','I','J','K','L','M','N','O', 'P','Q','R','S','T',
                'U','V','W','X','Y', 'Z', 'a','b','d','e','f','g','h','n','q','r','t']

    f = open('testingData.json')
    data = json.load(f)

    class_dict= {}
    data_dict = {}
    counter = 0
  
    for entry in data['entries']:
        data_dict[entry['file_name']] = entry['class']

    for dig in digits:
        class_dict[dig]=counter
        counter = counter + 1

    names = [name for name in data_dict]
    labels = [label for label in class_dict]
   
    # open and clean the cvs file up so
    # that is it ready for a fresh set of data points
    file = open("test_data.csv","r+")
    file.truncate(0)
    file.close()

    location = 0
    #iterate through each image in images/
    for image in names:
        # read the image in
        my_path = "preprocessed/" + image
        original = cv.imread(my_path,0)
        if original is None:
          print("Cannot find the image")
        
        # make sure it's the right shape
        img = original.reshape(28,28)

        # we need to save the image using 
        # the pillow library to iterate through
        # its pixels
        im = Image.fromarray(img)
        #new_name = "images/" + image
        #im.save(new_name, 'JPEG')
        #img = Image.open(new_name)
        
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
    

#main function 
if __name__ == '__main__':
    main()
