# Author: Floriana Ciaglia
# Date: July 12, 2020
# This file will execute the code base pipeline

from src.crop_fields import crop_fields
from src.form_alignment import form_alignment
from src.crop_bbox import crop_bbox
from src.char_detection import char_detection
from src.img_preprocessing import img_preprocessing
from src.img_preprocessing import img_test_preprocessing
from src.create_csv import create_csv
from src.create_csv import create_test_csv
from src.google_vision import google_vision_char_detection
from src.combine_results import combine 
from src.exit_exec import align_exit
from src.exit_exec import crop_exit
from src.exit_exec import char_exit
from src.exit_exec import preprocess_exit

import argparse
import os
import cv2


def main():

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", action='store_true',
        help="signals to run the pipeline. If not specified the Google API runs.")

    ap.add_argument("-i", "--input", required=True,
        help="path to Forest Service form")

    ap.add_argument("-json", "--coord", type=str, required=True,
        help="path to JSON file with fields coordinates")

    ap.add_argument("-temp", "--template", type=str, required=True,
        help="path to template form for form alignment")

    ap.add_argument("-t",  action='store_true',
        help="Testing pipeline execution flag. If not specified, the program executes in production mode")

    ap.add_argument("-combine",  action='store_true',
        help="Combine pipeline and google API flag. Both programs will be run and the outputs will be combined.")

    ap.add_argument("-align",  action='store_true',
        help="Stops the execution after form alignment and saves the aligned form to a new file.\n" + 
        "If not specified, the program executes until completion")

    ap.add_argument("-crop",  action='store_true',
        help="Stops the execution after crop field step and saves the cropped fields inside a new" +
        "directory.\n If not specified, the program executes until completion")

    ap.add_argument("-char",  action='store_true',
        help="Stops the execution after character detection and saves the single characters inside a " +
        "new directory.\n If not specified, the program executes until completion")

    ap.add_argument("-preprocess",  action='store_true',
        help="Stops the execution after image preprocessing and saves the proprocessed images inside a " +
        "new directory.\n If not specified, the program executes until completion")
    
    args = vars(ap.parse_args())

    # load input image
    form = cv2.imread(args["input"])

    # load template image
    temp = cv2.imread(args["template"])

    # check for wrong flag settings
    if args['p'] is True and args['combine'] is True:
        print("Error: you can't set the pipeline (-p) flag and the combine (-combine) flag at the same time.")
        exit()
    
    if args['t'] is False:
      
        # 1) the first step consists in aligning the form
        # we want to process with one of our templates in 
        # order to be able to work with know xy-coordinates 
        aligned = form_alignment(temp, form)

        if args['align'] is True:
            align_exit(aligned)
            exit()

        # 2) Once we have an aligned form, we crop each field
        # box out of the image and pass it to character detection
        field_imgs = crop_fields(args, aligned)

        if args['crop'] is True: 
            crop_exit(field_imgs)
            exit()

        # if the program was run with the -d [default] flag, 
        # the Google Vision APi executes and write the results to
        # a json file.
        if args['p'] is True:
            

            # 3) Now that we have field images, we  
            # detect single characters in the fields 
            # and crop single characters images out of the field
            single_chars = find_single_chars(field_imgs)

            if args['char'] is True:
                char_exit(single_chars)
                exit()

            # 4) Finally, we pre process each single character
            # image to minimize noise and refine the pen stroke.
            preprocessed_imgs = img_preprocessing(single_chars)
            

            if args['preprocess'] is True:
                preprocess_exit(preprocessed_imgs)
                exit()

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

    if args['p'] is False or args['combine'] is True:
        google_vision_char_detection(field_imgs)
        print("The Google Vision API results have been saved in the google_vision_results.json file.")

    if args['combine'] is True:
        print("Combination of results in progress...")
        combine()

    return 0


def find_single_chars(field_imgs):
    single_chars = []
    for image, field_name in field_imgs:
        # print(field_name)
        on_field_single_chars = char_detection(image, field_name)
        single_chars.extend(on_field_single_chars)

    return single_chars



#main function
if __name__ == '__main__':
  main()
