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
import os.path
from os import path

def main():
    # image names
    image_name = [('r_l.png', 'r'), ('o_l.png', 'O'), ('lower_case_s.png', 'S')]
    # create a dictionary to map each letter/digit to a number 
    
    digits = ['0', '1','2','3','4','5','6','7','8','9', 'A','B','C','D','E',
                'F','G','H','I','J','K','L','M','N','O', 'P','Q','R','S','T',
                'U','V','W','X','Y', 'Z', 'a','b','d','e','f','g','h','n','q','r','t']
  
    label_dict = {}
    counter = 0
    
    for dig in digits:
        label_dict[dig]=counter
        counter = counter + 1

    names = [name[0] for name in image_name]
    labels = [label[1] for label in image_name]

    file = open("test_data.csv","r+")
    file.truncate(0)
    file.close()

    location = 0
    #iterate through each image in images/
    for image in names:
        # read the image in
        my_path = "images/" + image
        original = cv.imread(my_path,0)
        
        #binary thresholding takes the image to balck and white
        ret, binaryThresh = cv.threshold(original,127,255,cv.THRESH_BINARY_INV)
        
        # make sure it's the right shape
        img = binaryThresh.reshape(28,28)
        im = Image.fromarray(img)
        
        new_name = "images/" + image
        im.save(new_name, 'JPEG')
     
        img = Image.open(new_name)
        
        pix = []
        
        pix.append(label_dict[labels[location]])
     

        #iterate through each pixel in the image and store its RBG value into a list
        for x in range(28):
            for y in range(28):
                rbg_val = img.getpixel((x,y))
                
                pix.append(rbg_val)
      
        with open('test_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(pix)
            file.close()
        location = location + 1
    

#main function 
if __name__ == '__main__':
    main()