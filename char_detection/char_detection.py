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
from PIL import Image
from queue import LifoQueue


def main():
    preprocessed_img = img_preprocess()
    find_char(preprocessed_img)
  

#  This function opens an image and detects
#  each character in it
def img_preprocess():
    #read data from JSON file
    f = open("fields.json")
    fields = json.load(f)

    #if it doesn't exists already, create the 
    # folder where the preprocessed images will go
    if not os.path.exists('preprocessed'):
        os.makedirs('preprocessed')

    directory = '/Users/florianaciaglia/Google Drive/AdaptLab/forestService/OCR_4_Forest_Service/char_detection/output'

    #for each image in the output directory:
    for image in os.listdir(directory):
        #set up the right string for the path 
        path = "output/" + image

        # read in the image in gray scale
        img = cv2.imread(path, 0) 
        if img is None:
            print(path)
            exit(1)

        #perform the image preprocessing stepss
        blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
        con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)

        return dst


def find_char(dst):
    max_x, max_y, min_x, min_y = 0, 0, 1000, 1000
    active = False
    stack = []
    im = Image.fromarray(dst)
    pixels = im.load()
    x = 0
    #iterate through the pixels in dst
    for x in range(im.size[0]): # for every pixel:
        #print("getting in hwew")
        for y in range(im.size[1]):
            #print("getting in here")
            
            #if the pixel is black
            if pixels[x,y] == (0, 0, 0):
                # do nothing
                continue

            else: #we found the first non-black pixel
                max_x, max_y, min_x, min_y = explore_active(x, y, im, pixels, stack, max_x, max_y, min_x, min_y)
                # 
                # print("# max x: ", max_x)
                # print("# max y: ", max_y)
                # print("# min x: ", min_x)
                # print("# min y: ", min_y)
                pixels[min_x, min_y] = (255, 0 , 0)
                pixels[max_x, min_y] = (255, 0 , 0)
                pixels[min_x, max_y] = (255, 0 , 0)
                pixels[max_x, max_y] = (255, 0 , 0)

        
            
        if max_x < im.size[0]-1:
            x = max_x + 2
            y = 0
            # break

        # print("# max x: ", max_x)
        # print("# max y: ", max_y)
        # print("# min x: ", min_x)
        # print("# min y: ", min_y)
    
        # break
        # print("before showing")
    # print("# max x: ", max_x)
    # print("# max y: ", max_y)
    # print("# min x: ", min_x)
    # print("# min y: ", min_y)
    # #  marking the corner of each bbox red
    # pixels[min_x, min_y] = (255, 0 , 255)
    # pixels[max_x, min_y] = (255, 0 , 255)
    # pixels[min_x, max_y] = (255, 0 , 255)
    # pixels[max_x, max_y] = (255, 0 , 255)    
    im.show()



def explore_active(x, y, im, pixels, stack, max_x, max_y, min_x, min_y):
    #  max_x, max_y, min_x, min_y
   
    # Initializing a values
    
    # max_x = 0
    # max_y = 0
    # min_x = 10000
    # min_y = 10000
    jump_size = 1

    stack.append((x,y))

    # while the stack holds tuples
    while len(stack) != 0:
        #print("Stack at beginning : ", stack)

        pair = stack.pop(len(stack)-1)
        print("pair: ", pair[0], pair[1])
        # if the pixel is already green, we have already visited it
        if pixels[pair[0], pair[1]] == (0, 255, 0):
            break

        # check to the right
        if look_right(pair[0], pair[1], im, pixels, jump_size):
            
            if pair[0] < im.size[0]-jump_size:
                stack.append((pair[0]+jump_size,pair[1]))
                max_x, min_x, max_y, min_y = check_coord(pair[0]+jump_size, pair[1], max_x, min_x, max_y, min_y)
     
            elif pair[0] >= im.size[0]-jump_size and pair[0] < im.size[0]-1:    
                stack.append((pair[0]+1,pair[1])) 
                max_x, min_x, max_y, min_y = check_coord(pair[0]+1, pair[1], max_x, min_x, max_y, min_y)     
            else:
                stack.append((pair[0],pair[1]))
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)
                    
            
            print("coords: ", max_x, min_x, max_y, min_y )

        # check down-wards
        if look_down(pair[0], pair[1], im, pixels, jump_size):
            

            if pair[1] < im.size[1]-jump_size:
                stack.append((pair[0],pair[1]+jump_size))
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1]+jump_size, max_x, min_x, max_y, min_y)
            elif pair[1] >= im.size[1]-jump_size and pair[1] < im.size[1]-1:    
                stack.append((pair[0],pair[1]+1))   
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1]+1, max_x, min_x, max_y, min_y)   
            else:
                stack.append((pair[0],pair[1]))
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            # max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)
            print("coords: ", max_x, min_x, max_y, min_y )

        # check to the left 
        if look_left(pair[0], pair[1], im, pixels, jump_size):

            if pair[0] > jump_size:
                stack.append((pair[0]-jump_size,pair[1]))  
                max_x, min_x, max_y, min_y = check_coord(pair[0]-jump_size, pair[1], max_x, min_x, max_y, min_y)

            elif pair[0] <= jump_size and pair[0] >= 0 :
                stack.append((pair[0]-1,pair[1]))
                max_x, min_x, max_y, min_y = check_coord(pair[0]-1, pair[1], max_x, min_x, max_y, min_y)
            else:
                stack.append((pair[0],pair[1]))
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            # max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)
            print("coords: ", max_x, min_x, max_y, min_y )

        # check up-wards
        if look_up(pair[0], pair[1], im, pixels, jump_size):
            
            print("in the look up if st")
            if pair[1] > jump_size:
                stack.append((pair[0],pair[1]-jump_size))  
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1]-jump_size, max_x, min_x, max_y, min_y)
            elif pair[1] <= jump_size and pair[1] >= 0 :
                stack.append((pair[0],pair[1]-1))
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1]-1, max_x, min_x, max_y, min_y)
            else:
                stack.append((pair[0],pair[1]))
                max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)
                
            # max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)
            print("coords: ", max_x, min_x, max_y, min_y )
        
        #turn the pixel green to sign it as visited
        pixels[pair[0], pair[1]] = (0, 255, 0)
        #print("Stack at end of loop: ", stack)

        # stack.remove(pair)
        #im.show()print("Stack at the end: ", stack)
    #print("Stack at exit: ", stack)
    return max_x, max_y, min_x, min_y

def x_in_bound(x, im):
    if x >= 0 and x <= im.size[0]-1:
        return True
    else:
        return False

def y_in_bound(y, im):
  
    if y >= 0 and y <= im.size[1]-1:
        return True
    else:
        return False


def look_right(x, y, im, pixels, jump_size):
    print("inside look right")
    print(x)
    print(y)

    retVal = False
    # check if x and y are in bound
    if x_in_bound(x, im) and y_in_bound(y, im):
        if x < im.size[0]-jump_size:
            if pixels[x+jump_size, y] != (0, 0, 0):
                retVal = True
        elif x >= im.size[0]-jump_size and x < im.size[0]-1:       
            if pixels[x+1, y] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
             retVal = True

    return retVal


def look_left(x, y, im, pixels, jump_size):
    print("inside look left")
    print(x)
    print(y)
    retVal = False
     
    if x_in_bound(x, im) and y_in_bound(y, im):
        
        if x > jump_size:
            if pixels[x-jump_size, y] != (0, 0, 0):
                retVal = True
        elif x <= jump_size and x >= 0:       
            if pixels[x-1, y] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
             retVal = True

    return retVal

def look_down(x, y, im, pixels, jump_size):
    print("inside look down")
    print(x)
    print(y)
    
    retVal = False
    if x_in_bound(x, im) and y_in_bound(y, im):
        if y < im.size[1]-jump_size:
            if pixels[x, y+jump_size] != (0, 0, 0):
                retVal = True
        elif y > im.size[1]-jump_size and y < im.size[1]-1:       
            if pixels[x, y+1] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
             retVal = True

    return retVal


def look_up(x, y, im, pixels, jump_size):
    print("inside look up")
    print(x)
    print(y)
    retVal = False

    if x_in_bound(x, im) and y_in_bound(y, im):
        if y > jump_size:
            if pixels[x, y-jump_size] != (0, 0, 0):
                retVal = True
        elif y <= jump_size and y >= 0:       
            if pixels[x, y-1] != (0, 0, 0): 
                retVal = True
        else:       
            if pixels[x, y] != (0, 0, 0):
             retVal = True

    print("retVal: " , retVal)
    return retVal


def check_coord(x, y, max_x, min_x, max_y, min_y):
  if x > max_x:
    max_x = x
  
  if x < min_x:
    min_x = x
    
  if y > max_y:
    max_y = y
   
  if y < min_y:
    min_y = y
  
  return max_x, max_y, min_x, min_y



# main function
if __name__ == '__main__':
    main()