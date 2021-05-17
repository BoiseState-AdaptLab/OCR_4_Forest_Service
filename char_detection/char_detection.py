# Author: Floriana Ciaglia
# Date: May 14th, 2021

# This program attempts to create a bounding box around a discrete letter by:
#       - take a field image as an input
#       - iterate through each pixel in the image
#       - keep track of max x, max y, min x, min y

import cv2
import json
import shutil
import os

def main():
    window_name = "image"
    i = 0
    # open file as an image
    img = cv2.imread('highRes_ForestService.jpg')

    # load the json file
    json_file = open('fields.json')
    fields = json.load(json_file)

    if os.path.exists('output'):
        try:
            shutil.rmtree('output')
        except:
            #print("Error: %s : %s" % ('output', e.strerror))
            print("Didn't work")

    if not os.path.exists('output'):
        os.makedirs('output')

    for field in fields['fields']:
        # print(field)
        x = int(field['coord_pixel'][0])
        y = int(field['coord_pixel'][1])
        w = int(field['width'])
        h = int(field['height'])

        # cropping the image
        cropped_img = crop(img, x, y, w, h)

        # display the image to user
        if cropped_img is not None:
            cv2.imshow(window_name, cropped_img)
            cv2.imwrite('field_{num}.jpg'.format(num = i), cropped_img)
            old_path = os.path.abspath('field_{num}.jpg'.format(num = i))
            new_path = old_path[:-12] + "/output/"
            shutil.move(old_path, new_path)
        else:
            print("no image has been read")

        i += 1

        json_file.close()

    exit(0)


# cropping function
def crop(image, x, y, w, h):
    cropped = image[y:y + h, x:x + w]

    return cropped


# main function
if __name__ == '__main__':
    main()