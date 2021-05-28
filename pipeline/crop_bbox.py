#   Author: Floriana Ciaglia
#   Date: May 24th, 2021

#   Description: This driver will open the JSON file and crop 
#   the bounding boxes out of the form.
import cv2
import os
import json
import shutil


def main():
    # clean the directory from previous data
    # or create it
    output_dir()

    # open json file bbox_coord.json with bbox coordinates
    fields = open_json()
  
    # iterate through fields and find the bboxes
    crop(fields)

    # the new images generated are stored in the single_chars/ directory
        
    exit(0)

"""
Load the data from the bbox coord file
"""
def open_json():
    # load the json file
    json_file = open('bbox_coord.json')
    fields = json.load(json_file)
    return fields


"""
 if the output dir already exists, it gets
 cleaned up. Otherwise, it gets created 
"""
def output_dir():
    # if it already exists, clean it
    if os.path.exists('single_chars'):
        try:
            shutil.rmtree('single_chars')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('single_chars'):
        os.makedirs('single_chars')


"""
Iterates through fields and marks the min and max of bbox
around a character
"""
def crop(fields):
    DIR = 'fields/'
    i = 0

    for dict in fields:
     
        # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)
        
        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    # cv2.imshow(window_name, cropped_img)
                    cv2.imwrite('box_{num}.jpg'.format(num = i), cropped_img)

                    old_path = os.path.abspath('box_{num}.jpg'.format(num = i))
                    new_path = old_path[:-10] + "/single_chars/"
                    shutil.move(old_path, new_path)
                else:
                    print("no image has been read")

                i = i + 1 



"""
Definition of main function
"""
if __name__ == '__main__':
    main()


