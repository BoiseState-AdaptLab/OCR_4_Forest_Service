# Author: Floriana Ciaglia
# Data: March 8, 2021
# https://yangcha.github.io/iview/iview.html
import cv2
import os
import string
import json
import shutil


def main():
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
        json_file = open('all_fields.json')
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
            x = (field['coord_pixel'][0])
            y = (field['coord_pixel'][1])
            w = field['width']
            h = field['height']

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

        json_file.close()
    exit(0)


# cropping function
def crop(image, x, y, w, h):
    cropped = image[y:y + h, x:x + w]

    return cropped


# function to resize found on https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv

# main function
if __name__ == '__main__':
    main()
