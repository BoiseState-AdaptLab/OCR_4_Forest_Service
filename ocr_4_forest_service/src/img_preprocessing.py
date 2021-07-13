# Author: Floriana Ciaglia
# Date: May 1st, 2021
# This script preprocesses the single letter images from the Forest Service Form and create 
# the csv file that will work as input for the OCR model. 

import cv2
import os
from os import path 


def img_preprocessing():

    DIR = 'single_chars/'

    # if it doesn't exists already, create the 
    # folder where the preprocessed images will go
    if not os.path.exists('preprocessed'):
        os.makedirs('preprocessed')


    for image in os.listdir(DIR):
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


   
