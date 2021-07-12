# Author: Floriana Ciaglia
# Data: May 13th, 2021

import cv2
import os
import string
import json
import csv
import shutil
import numpy as np
from matplotlib import pyplot as plt
from os import path 
import PIL
from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter
from PIL import ImageEnhance
from IPython.display import display

def main():
    #######################################################
    # Step 1)                                             #
    # Open json file and crop the fields out of the form  #
    #######################################################

    path = None
    window_name = "image"
    i = 0
    # prompt user for input
    if (path is not 'q'):
        path = input("Enter the path to the Forest Service Sheet or type q to quit: ")

        while not os.path.isfile(path):

            if path == 'q':
                exit(0)
            path = input("** The file could not be found ** \n Enter a valid path to the file: ")

        # open file as an image
        img = cv2.imread(path)

        # load the json file
        json_file = open('high_res.json')
        data = json.load(json_file)

        if os.path.exists('output'):
          try:
            shutil.rmtree('output')
          except:
            print("Error while removing directory")
            

        if not os.path.exists('output'):
          os.makedirs('output')

        for field in data['character']:
            # print(field)
            x = int(field['x'])
            y = int(field['y'])
            w = int(field['w'])
            h = int(field['h'])
  
            # cropping the image
            cropped_img = crop(img, x, y, w, h)

            # display the image to user
            if cropped_img is not None:
                cv2.imshow(window_name, cropped_img)
                cv2.imwrite('field_{num}.jpg'.format(num = i), cropped_img)

                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                old_path = os.path.abspath('field_{num}.jpg'.format(num = i))
                new_path = old_path[:-12] + "/output/"
                shutil.move(old_path, new_path)
            else:
                print("no image has been read")

            i += 1
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            #cv2.destroyWindow(window_name)
            #cv2.waitKey(10)

        ################################################
        # Step 2)                                      #
        # Image pre processing                         #
        # ############################################## 

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

            #perform preprocessing steps
            preprocess(img, image)

            

        ################################################
        # Step 3)                                      #
        # Formatting the data and storing it in a csv. #
        ################################################

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
            original = cv2.imread(my_path,0)
            if original is None:
                print("Cannot find the image")
            
            # make sure it's the right shape
            img = cv2.resize(original, (28,28))

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


    exit(0)


# cropping function
def crop(image, x, y, w, h):
    cropped = image[y:y + h, x:x + w]

    return cropped

#perform preprocessing steps
def preprocess(img, name):
    if img is None:
        print(path)
        exit(1)

    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
    dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)

    end_path = "preprocessed/" + name
    cv2.imwrite(end_path, dst)



# function to resize found on https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv

# main function
if __name__ == '__main__':
    main()