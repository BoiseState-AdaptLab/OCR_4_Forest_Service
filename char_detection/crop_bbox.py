#   Author: Floriana Ciaglia
#   Date: May 24th, 2021

#   Description: This driver will open the JSON file and crop 
#   the bounding boxes out of the form.
import cv2
import os
import string
import json
import shutil


def main():
    path = None
    window_name = "image"
    i = 0
   
    dir = 'output/'

    if os.path.exists('single_chars'):
        try:
            shutil.rmtree('single_chars')
        except:
            print("Didn't work")

    if not os.path.exists('single_chars'):
        os.makedirs('single_chars')

    # load the json file
    json_file = open('bbox_coord.json')
    fields = json.load(json_file)
    # print(type(fields))
    # print(fields)
    for dict in fields:
        # print("type od dicts: ", type(dict))
        # print(dict)
        # print(" ")
        # print("the key is: ", dict.keys())
        key = dict.keys()
        # we only get the key
        new_d = [str(key) for key in key]
        # print(new_d[0])
        field_name = dir + new_d[0]
        # print(field_name)
        # open form as an image
        img = cv2.imread(field_name)
        
        for boxes in dict.values():
            # box is the list of bbox in one field image
            print(boxes)
            # print(box['x'])
            print("type of box: ", type(boxes))
            for box in boxes:
                print("x: ", box['x'])
                print("y: ", box['y'])
                print("w: ", box['w'])
                print("h: ", box['h'])

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = crop(img, x, y, w, h)

                # display the image to user
                if cropped_img is not None:
                    cv2.imshow(window_name, cropped_img)
                    cv2.imwrite('box_{num}.jpg'.format(num = i), cropped_img)

                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    old_path = os.path.abspath('box_{num}.jpg'.format(num = i))
                    new_path = old_path[:-12] + "/output/"
                    shutil.move(old_path, new_path)
                else:
                    print("no image has been read")

                i += 1
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # cv2.destroyWindow(window_name)
                # cv2.waitKey(10)

            json_file.close()
    exit(0)


# cropping function
def crop(image, x, y, w, h):
    cropped = image[y:y + h, x:x + w]

    return cropped


# main function
if __name__ == '__main__':
    main()


