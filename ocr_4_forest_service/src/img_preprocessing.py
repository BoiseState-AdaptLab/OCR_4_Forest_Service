# Author: Floriana Ciaglia
# Date: May 1st, 2021
# This script preprocesses the single letter images from the Forest Service Form and create 
# the csv file that will work as input for the OCR model. 

import cv2
import os
from os import path 
import shutil


def img_preprocessing():

    DIR = 'single_chars/'

    # if it doesn't already exist, create the 
    # folder where the preprocessed images will go
    output_dir()


    for image in os.listdir(DIR):
        #set up the right string for the path 
        path = "single_chars/" + image

        # read in the image in gray scale
        img = cv2.imread(path, 0) 
        if img is None:
            print(path)
            exit(1)

        ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    

        con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)
       
        resized = cv2.resize(dst, (28,28))
  
        end_path = "preprocessed/" + image
        cv2.imwrite(end_path, resized)


   
    
"""
 if the output dir already exists, it gets
 cleaned up. Otherwise, it gets created 
"""
def output_dir():
    # if it already exists, clean it
    if os.path.exists('preprocessed'):
        try:
            shutil.rmtree('preprocessed')
        except:
            print("Error: couldn't clean the preprocessed/ directory")
    # else, create it
    if not os.path.exists('preprocessed'):
        os.makedirs('preprocessed')