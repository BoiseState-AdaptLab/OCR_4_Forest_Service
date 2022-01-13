# Author: Floriana Ciaglia
# Date: Jan 13, 2022
# This file contains the functions to call when we want to stop the execution mid-pipeline

import cv2
import argparse
import os

# global var for current directory
curr_dir = os.getcwd()

def align_exit(aligned_form):
    cv2.imwrite('aligned-form.jpg', aligned_form)
    print("Pipeline executed until after form alignment step."+ 
            "\n\t-The aligned form has been saved to this directory.")


def crop_exit(field_imgs):
    new_dir = 'cropped_fields'
    path = curr_dir + '/' + new_dir
    isExist = os.path.exists(path)

    # create the dir where to store cropped images, 
    # if it doesn't exist already
    if not isExist:
        os.mkdir(os.path.join(curr_dir, new_dir))
    else: # delete old files
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    
    for image in field_imgs:
        img_name = image[1] + '.jpg'
        cv2.imwrite(os.path.join(path , img_name), image[0])
    print("Pipeline executed until after crop fields step." +
            "\n\t-The cropped images have been saved inside the /cropped_fields directory.")


def char_exit(single_chars):
    new_dir = 'char_detection'
    path = curr_dir + '/' + new_dir
    isExist = os.path.exists(path)

    # create the dir where to store cropped images, 
    # if it doesn't exist already
    if not isExist:
        os.mkdir(os.path.join(curr_dir, new_dir))
    else: # delete old files
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

    counter = 0
   
    for pair in single_chars:
        img_name = pair[1] + '-' + str(counter) + '.jpg'
        cv2.imwrite(os.path.join(path , img_name), pair[0])
        counter = counter + 1


    print("Pipeline executed until after character detection step." +
            "\n\t-The cropped images have been saved inside the /char_detection directory.")



def preprocess_exit(preprocessed_imgs):
    new_dir = 'img_preprocessing'
    path = curr_dir + '/' + new_dir
    isExist = os.path.exists(path)

    # create the dir where to store cropped images, 
    # if it doesn't exist already
    if not isExist:
        os.mkdir(os.path.join(curr_dir, new_dir))
    else: # delete old files
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

    counter = 0
    
    for pair in preprocessed_imgs:
        img_name = pair[1] + '-' + str(counter) + '.jpg'

        cv2.imwrite(os.path.join(path , img_name), pair[0])
        counter = counter + 1
    print("Pipeline executed until after image preprocessing step. \n\t-The cropped images have been saved inside the /img_preprocessing directory.")

