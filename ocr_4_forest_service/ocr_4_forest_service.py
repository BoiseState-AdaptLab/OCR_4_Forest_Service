# Author: Floriana Ciaglia
# Date: July 12, 2020
# This file will run the production pipeline

from src.crop_fields import crop_fields
from src.form_alignment import form_alignment
from src.crop_bbox import crop_bbox
from src.char_detection import char_detection
from src.img_preprocessing import img_preprocessing
from src.img_preprocessing import img_test_preprocessing
from src.create_csv import create_csv
from src.create_csv import create_test_csv
import argparse
import cv2


def main():

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
        help="path to Forest Service form")
    ap.add_argument("-json", "--coord", type=str, required=True,
        help="path to JSON file with fields coordinates")
    ap.add_argument("-temp", "--template", type=str, required=True,
        help="path to template form for form alignment")
    ap.add_argument("-t",  action='store_true',
        help="Testing pipeline execution flag. If not specified, the program executes in production mode")
    args = vars(ap.parse_args())

    # the main functions are called in order of execution
    # determined by the pipeline

    if args['t'] is False:
        # 1) the first step consists in aligning the form
        # we want to process with one of our templates in 
        # order to be able to work with know xy-coordinates 
        aligned = form_alignment(args)

        # 2) Once we have an aligned form, we crop each field
        # box out of the image and generate the new images in
        # a new directory 
        field_imgs = crop_fields(args, aligned)

        # 3) Now that we have field images, we  
        # detect single characters in the fields 
        # and generate a JSON file with the coordinates
        # of the detected characters
        single_chars = []
        for image in field_imgs:
            on_field_single_chars = char_detection(image)
            single_chars.extend(on_field_single_chars)

        # 4) Finally, we pre process each single character
        # image to minimize noise and refine the pen stroke.
        preprocessed_imgs = img_preprocessing(single_chars)

        # 6) This last step will generate a csv file with the RGB 
        # value of each pixel in the image - this csv file will
        # be the input for the Optical Character Recognition model. 
        create_csv(preprocessed_imgs)
        
        print("Done Executing Production Pipeline!")
        
    else: # The program is being run in testing mode.
          # The execution will be similar to the 
          # production mode except for classifications. 

        # 1) We begin the execution from the bounding box 
        # cropping because the JSON file provided was 
        # manually generated to incorpotate single characters.
        single_chars = crop_bbox(args)

        # 2) From this step onward, the execution is the same 
        # as the production pipeline.
        preprocessed_imgs = img_test_preprocessing(single_chars)

        # 3) Instead of hard-coding the classification to zero
        # in the csv file, in the testing pipeline we know the
        # correct classifications to store in the csv file. 
        create_test_csv(preprocessed_imgs)

        print("Done Executing Testing Pipeline!")
        

        
#main function
if __name__ == '__main__':
  main()
