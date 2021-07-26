# Author: Floriana Ciaglia
# Date: May 1st, 2021
# This script preprocesses the single letter images from the Forest Service Form and create 
# the csv file that will work as input for the OCR model. 

import cv2
import os
from os import path 
import shutil


def img_preprocessing(list_single_chars):
    preprocessed = []
    for image in list_single_chars:

        ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    

        con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)

        padded = add_padding(dst)
       
        resized = cv2.resize(padded, (28,28))
        preprocessed.append(resized)
  
    return preprocessed



def img_test_preprocessing(list_single_chars):

    preprocessed = []
    for (image, classi) in list_single_chars:
        # print(type(image))
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    

        con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)

        padded = add_padding(dst)
       
        resized = cv2.resize(padded, (28,28))
        preprocessed.append((resized, classi))

    
    return preprocessed 


def add_padding(im):

    color = [0, 0, 0] # padding in black
    new_im = cv2.copyMakeBorder(im, 4, 4, 4, 4, cv2.BORDER_CONSTANT,
        value=color)
    
    return new_im


