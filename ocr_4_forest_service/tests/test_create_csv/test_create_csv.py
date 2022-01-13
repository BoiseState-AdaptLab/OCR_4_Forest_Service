# this file contains the functions that test the create_csv functionality

from ...src.create_csv import create_csv
import os
import csv
import cv2

def test_create_csv():

    preprocessed_imgs = []
    img = cv2.imread('thresh.png')
    preprocessed_imgs.append(img)    
    create_csv(preprocessed_imgs)

    # count how many lines the csv file has
    # and assert that they match with the 
    # amount of images stored in preprocessed/

    file = open("test_data.csv")
    reader = csv.reader(file)
    lines= len(list(reader))

    
    assert len(preprocessed_imgs) == lines
