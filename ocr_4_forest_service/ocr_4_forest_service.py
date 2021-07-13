# Author: Floriana Ciaglia
# Date: July 12, 2020
# This file will run the entire pipeline

from src.crop_fields import crop_fields
from src.form_alignment import form_alignment
from src.crop_bbox import crop_bbox
from src.char_detection import char_detection
from src.img_preprocessing import img_preprocessing
from src.create_csv import create_csv
import argparse

def main():

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
        help="path to Forest Service form")
    ap.add_argument("-json", "--coord", type=str, required=True,
        help="path to JSON file with fields coordinates")
    ap.add_argument("-temp", "--template", type=str, required=True,
        help="path to template form for form alignment")
    args = vars(ap.parse_args())

    # the main functions are called in order of execution
    # determined by the pipeline

    # 1) the first step consists in aligning the form
    # we want to process with one of our templates in 
    # order to be able to work with know xy-coordinates 
    form_alignment(args)

    # 2) Once we have an aligned form, we crop each field
    # box out of the image and generate the new images in
    # a new directory 
    crop_fields(args)

    # 3) Now that we have field images, we  
    # detect single characters in the fields 
    # and generate a JSON file with the coordinates
    # of the detected characters
    char_detection()

    # 4) We read the newly generated JSON file and crop
    # the single character images out of the fields and 
    # store them into a new directory
    crop_bbox()

    # 5) Finally, we pre process each single character
    # image to minimize noise and refine the pen stroke.
    
    img_preprocessing()

    # 6) This last step will generate a csv file with the RGB 
    # value of each pixel in the image - this csv file will
    # be the input for the Optical Character Recognition model. 
    create_csv()
    
    print("Done Executing Production Pipeline!")


#main function
if __name__ == '__main__':
  main()
