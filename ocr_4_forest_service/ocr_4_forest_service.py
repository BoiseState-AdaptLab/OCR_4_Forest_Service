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
import argparse
import os
import cv2

# global var for current directory
curr_dir = os.getcwd()

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
    ap.add_argument("-align",  action='store_true',
        help="Stops the execution after form alignment and saves the aligned form to a new file.\n If not specified, the program executes until completion")
    ap.add_argument("-crop",  action='store_true',
        help="Stops the execution after crop field step and saves the cropped fields inside a new directory.\n If not specified, the program executes until completion")
    ap.add_argument("-char",  action='store_true',
        help="Stops the execution after character detection and saves the single characters inside a new directory.\n If not specified, the program executes until completion")
    ap.add_argument("-preprocess",  action='store_true',
        help="Stops the execution after image preprocessing and saves the proprocessed images inside a new directory.\n If not specified, the program executes until completion")
    
    args = vars(ap.parse_args())


    # load input image
    form = cv2.imread(args["input"])

    # load template image
    temp = cv2.imread(args["template"])

    # the main functions are called in order of execution
    # determined by the pipeline

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

        # 3) Now that we have field images, we  
        # detect single characters in the fields 
        # and crop single characters images out of the field
        single_chars = []
        for image, field_name in field_imgs:
          
            on_field_single_chars = char_detection(image, field_name)
            single_chars.extend(on_field_single_chars)
        
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
        


def align_exit(aligned_form):
    cv2.imwrite('aligned-form.jpg', aligned_form)
    print("Pipeline executed until after form alignment step. \n\t-The aligned form has been saved to this directory.")


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
    print("Pipeline executed until after crop fields step. \n\t-The cropped images have been saved inside the /cropped_fields directory.")


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


    print("Pipeline executed until after character detection step. \n\t-The cropped images have been saved inside the /char_detection directory.")



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
        # print(pair[1])

        cv2.imwrite(os.path.join(path , img_name), pair[0])
        counter = counter + 1
    print("Pipeline executed until after image preprocessing step. \n\t-The cropped images have been saved inside the /img_preprocessing directory.")



#main function
if __name__ == '__main__':
  main()
