# Author: Floriana Ciaglia
# Date: July 13, 2020
# File: This is the last step of our production pipeline where we reccord 
# all the RGB values of each pixel from each preprocessed image and store the 
# data into a csv file. 

from PIL import Image
import cv2
import os
from os import path 
import csv
import json

def create_csv():

    DIR = 'preprocessed/'

    # open and clean the cvs file up so
    # that is it ready for a fresh set of data points
    file = open("test_data.csv","w")
    file.truncate(0)
    file.close()

   
    for image in os.listdir(DIR):
        path = 'preprocessed/'+image
        # print(image)
        img = cv2.imread(path, 0)
        if img is None:
            print("Cannot find image: ", path)

        # we need to save the image using 
        # the pillow library to iterate through
        # its pixels
        im = Image.fromarray(img)

        #At this point, the image is ready
        #list of RGB values for each pixel in the image
        pix = []

        # the first column in the csv file is the image classification
        # Since, we don't know what that is, we hard code it to zero. 
        pix.append(0)
    

        #iterate through each pixel in the image and store its RBG value into a list
        for x in range(28):
            for y in range(28):
                rbg_val = im.getpixel((x,y))
                pix.append(rbg_val)
    
        with open('test_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(pix)
            file.close()


# This version of the function will 
# create a csv file with the RGB values
# of each pixel of the image and its classification    
def create_test_csv(args):

    #read data from JSON file
    f = open(args["coord"])

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

    # open and clean the cvs file up so
    # that is it ready for a fresh set of data points
    file = open("test_data.csv","w")
    file.truncate(0)
    file.close()

  
    for image in names:

        #set up the right string for the path 
        path = "preprocessed/" + image

        # read in the image in gray scale
        img = cv2.imread(path, 0) 
        if img is None:
            # print("here")
            print(path)
            exit(1)

        
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
    

        #iterate through each pixel in the image and store its RBG value into a list
        for x in range(28):
            for y in range(28):
                rbg_val = im.getpixel((x,y))
                pix.append(rbg_val)
    
        with open('test_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(pix)
            file.close()
       