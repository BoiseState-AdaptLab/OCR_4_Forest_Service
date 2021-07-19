# Author: Floriana Ciaglia, Joshua Suotelo Vieira
# Date: May 14th, 2021

# This program creates a bounding box around a discrete letter by:
#       - take a field image as an input
#       - iterate through each pixel in the image
#       - keep track of max x, max y, min x, min y

# Generates a JSON file called bbox_coord.json the coordinates of each detected bounding box

import cv2
import json
import os
import os.path
from os import path
from PIL import Image
from queue import LifoQueue
import numpy as np

"""
Definition of the main fuction
"""
def char_detection():
    img_preprocess()
    json_file = word_segmentation()
    create_json(json_file)
  

"""
Performs the image preprocessing on the field image 
before bounding boxes identification
"""
def img_preprocess():
    DIR = "fields/"

    # this is the list where 
    # each images data is stored 
    list_of_dict = []
    list_of_tracings = []

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("bbox_coord.json"):
        file = open("bbox_coord.json","r+")
        file.truncate(0)
        file.close()
  
    
    #for each image in the output directory:
    for image in os.listdir(DIR):
        print("in img_preprocessing: ", image)
        json_dict = {} 
        tracing_dict = {}
        #set up the right string for the path 
        path = DIR + image
        
        # read in the image in gray scale
        img = cv2.imread(path, 0) 
        if img is None:
            print(path)
            exit(1)
        
        #perform the image preprocessing stepss
        blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
      
        con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
        json_data, tracing_data = find_char(dst, image, json_dict, tracing_dict)
        # print(json_data)
        list_of_dict.append(json_data)
        # print(list_of_dict)
        list_of_tracings.append(tracing_data)


    with open('tracing_list.json', 'w') as convert_file:
        convert_file.write(json.dumps(list_of_tracings))

    create_json(list_of_dict)
    


"""
Iterates through the image until it finds a character. 
It explores the character to find its max_x, min_x, max_y, min_y
@return dictionary of data to populate the json file
"""
def find_char(dst, img, json_dict, tracing_dict):
     
    max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
    json_list = []
    tracing_list = []
    x = 0

    # Open the image using the PIL library
    im = Image.fromarray(dst)
    pixels = im.load()
    
    # clean the dictionary out 
    # before adding a new image
    json_dict.clear()
    i = 0
    #iterate through the pixels in dst
    while (x < im.size[0]): # for every pixel:
        y = 0
        
        while (y < im.size[1]):
            
            #if the pixel is white
            if pixels[x,y] != (0, 0, 0):
                
                max_x, min_x, max_y,  min_y = explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y)
                
                # if the area is big enough we identify it as a character
                if valid_area(max_x, max_y, min_x, min_y):
                    pixels[min_x, min_y] = (255, 0 , 0)
                    pixels[max_x, min_y] = (255, 0 , 0)
                    pixels[min_x, max_y] = (255, 0 , 0)
                    pixels[max_x, max_y] = (255, 0 , 0)

                    # im.show()
                    box_num = 'box_{num}'.format(num = i)
                    json_list.append({'box': box_num,
                                    'x': min_x, 
                                    'y': min_y, 
                                    'w': max_x-min_x,
                                    'h': max_y-min_y})
                    # print("json list: ", json_list)
                    # im.show()
                    tracing = get_tracing(im, pixels, max_x, min_x, max_y, min_y, box_num)
                    # print(" ", img, tracing)
                    tracing_list.append(tracing)
                    i = i + 1
                y = 0
                # exit()
                x = max_x + 2
                if x > im.size[0]-1:
                    y = im.size[1]
                max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
                

            else:
                y = y + 2
        
        x = x + 2
    # print(tracing_list)
    # print("len of tracing list: ", len(tracing_list))
    #All the characters have been identified
    tracing_dict[img] = tracing_list
    # print(tracing_dict)
    # exit()
    if valid_area(max_x, max_y, min_x, min_y):
        # print("we are in valid_area")
        json_dict[img] = json_list
    
    return json_dict, tracing_dict
 

"""
Accepts only the areas that are bigger than 100
@return boolean
"""
def valid_area(max_x, max_y, min_x, min_y):
    # calculate the area of the bbox to 
    # minimize noise
    width = max_x - min_x
    height = max_y - min_y
    area = width * height

    if area > 100:
        return True
    else:
        return False

 
"""
Creates the json file with the bbox coordinates
"""
def create_json(list_of_dict):
    
    # store the data into a new json file
    with open("bbox_coord.json", 'w') as outfile: 
        json.dump(list_of_dict, outfile)
    


"""
Checks the x axis boundary
@return boolean
"""    
def x_in_bound(x, im):

    if x >= 0 and x <= im.size[0]-1:
        return True
    else:
        return False

"""
Checks the y axis boundary
@return boolean
"""
def y_in_bound(y, im):
  
    if y >= 0 and y <= im.size[1]-1:
        return True
    else:
        return False


"""
Loops through all the pixels in the stack and colors them green when visited
@return min and max coordinates
"""
def explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y):
    # Initializing a values
    stack = []
    jump_size = 1
    stack.append((x,y))
    
    # while the stack holds tuples
    while len(stack) != 0:

        # pop the first pair off the stack
        pair = stack.pop(len(stack)-1)

        # if the pixel is already green, we have already visited it
        if x_in_bound(pair[0], im) and y_in_bound(pair[1], im) and pixels[pair[0], pair[1]] != (0, 255, 0):

            # check and update the bbox coordinates
            max_x, min_x, max_y, min_y = check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)

            # check to the right
            if look(pair[0]+jump_size, pair[1], im, pixels):
                stack.append((pair[0]+jump_size,pair[1]))

            # check down-wards
            if look(pair[0], pair[1]+jump_size, im, pixels):
                stack.append((pair[0],pair[1]+jump_size))

            # check to the left 
            if look(pair[0]-jump_size, pair[1], im, pixels):
                stack.append((pair[0]-jump_size,pair[1])) 

            # check up-wards
            if look(pair[0], pair[1]-jump_size, im, pixels):
                stack.append((pair[0],pair[1]-jump_size)) 
            
            #turn the pixel green to sign it as visited
            pixels[pair[0], pair[1]] = (0, 255, 0)

    # 
    # im.show()
    
    return max_x, min_x, max_y,  min_y


def get_tracing(im, pixels, max_x, min_x, max_y, min_y, box_num):
    # im.show()

    tracing = []
    tracing.append(box_num)
  
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            
            if pixels[x, y] == (0,  255, 0):
                tracing.append((x,y))
    
    # We now have the entire tracing of the character
    return tracing



"""
Looks if the neighbor pixels is available
"""
def look(x, y, im, pixels):

    retVal = False
    # check if x and y are in bound
    if x_in_bound(x, im) and y_in_bound(y, im):
        if pixels[x, y] != (0, 0, 0):
            retVal = True

    return retVal


"""
Updates the max and min coordinates
"""
def check_coord(x, y, max_x, min_x, max_y, min_y):
  if x > max_x:
    max_x = x
  
  if x < min_x:
    min_x = x
    
  if y > max_y:
    max_y = y
   
  if y < min_y:
    min_y = y

  return max_x, min_x, max_y,  min_y


def word_segmentation():

    # load the json file
    json_file = open('bbox_coord.json')
    letters = json.load(json_file)
    json_list = {}
    json_list = []

    for fields in letters:
        characters = {}
        char_points = []
        path = 'fields/' + list(fields.keys())[0]
        field_img = cv2.imread(path, 1)

        if field_img is None:
            print("Issues opening the image")
            exit(1)

        # print("fields : ", fields)
        
        for field_name, dicts in fields.items():
            # print("dicts : ", dicts)
             
            for box in dicts:
                # print("box: ", box)
                name = box['box']
                x = int(box['x'])
                y = int(box['y'])
                w = int(box['w'])
                h = int(box['h'])
                word_img = field_img[y:y+h, x:x+w]

                if word_img is None:
                    print("we had an issue reading the image ")

                # How many times does the height fits into the width?
                ratio = w / h 
                ratio_constrain=1.5
                width_constrain=40
                block_size=10
                step_size=5
                thresh=10

                # Condition to run the slicing character approach
                if ratio > ratio_constrain and w > width_constrain:
                    # Performs somre preprocessing to the image
                    gray_img = cv2.cvtColor(word_img, cv2.COLOR_BGR2GRAY)
                    _, thresh_img = cv2.threshold(gray_img, -0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
                    # Remove long horizontal lines
                    res_op_1 = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, np.ones((1, 40), np.uint8))
                    thresh_img -= res_op_1
                    # Calculate the image vertical projection histogram
                    word_v_hist_proj, word_h_hist_proj, v_hist_img, h_hist_img = create_h_v_image_proj(thresh_img)
                    # Get characters
                    if len(word_v_hist_proj) > block_size:
                        seg_points = segmentation_points(word_v_hist_proj, block_size, step_size, thresh)
                        # Improve segmentation positions
                        seg_points = local_search(word_v_hist_proj, seg_points, block_size // 2)
                        # Pixel transition count
                        seg_points = pixel_transition_count(thresh_img, seg_points)
                        # Update x coordinate in respect of original image
                        seg_points = [int(char_x + x) for char_x in seg_points]
                        # Keeps track of the original coordinates so then segmentation points
                        # can be converted to coordinates
                        if seg_points != []:
                            char_points.append({"orig_coords": box, "char_coords": seg_points})
                        else:
                            char_points.append(box)
                else:
                    char_points.append(box)

            # From segmentation lines to actual x, y, w, and h inside the field
            bbox_coords = []
            for chars in char_points:
                if "orig_coords" in chars.keys():
                    orig_x = chars['orig_coords']['x']
                    orig_y = chars['orig_coords']['y']
                    orig_h = chars['orig_coords']['h']
                    orig_w = chars['orig_coords']['w']
                    # Keeps track of the previous segmentation line x position 
                    prev_seg_line = orig_x
                    seg_lines = chars['char_coords']
                    for seg_line in seg_lines:
                        x = prev_seg_line
                        w = seg_line - prev_seg_line
                        y = orig_y
                        h = orig_h
                        bbox_coords.append({"box": name, "x": x, "y": y, "w": w, "h": h})
                        prev_seg_line = x + w
                        # Append the last one, from the segmentation line to the end of the
                        # field
                    w = (orig_x + orig_w) - (x + w)
                    bbox_coords.append({"box": name, "x": prev_seg_line, "y": y, "w": w, "h": h})
                else:
                    bbox_coords.append(chars)
                
                # Remove single pixel width characters (too small to be a character) 
                for coord in bbox_coords:
                    w = coord['w']
                    h = coord['h']
                    if w <= 2 or h <= 2:
                        bbox_coords.remove(coord)
                

            characters[field_name] = bbox_coords
      
        json_list.append(characters)
        
                    
    return json_list



def create_h_v_image_proj(thresh_img):
    """Create vertical and horizontal histogram projections and their 
    respective images.

    Parameters:
    thresh_img: 2D array that represent the pixel intensity value of an image
    that has been thresholded (0 or 255 pixel values)

    Returns:
    word_v_hist_proj: 1D array same size as width of thresh_img where each 
    element represents the white pixel frequency of one column of thresh_image
    word_h_hist_proj: 1D array same size as height of thresh_img where each 
    element represents the white pixel frequency of one row of thresh_image
    v_hist_img: 2D array representing in an image the vertical histrogram 
    projection
    h_hist_img: 2D array representing in an image the horizontal histrogram 
    projection
    """
    h, w = thresh_img.shape[:2]
    # Creates black image same size as thresh_img
    h_hist_img = np.zeros(thresh_img.shape[:2], dtype='uint8')
    v_hist_img = np.zeros(thresh_img.shape[:2], dtype='uint8')
    # Normalizes the image and counts pixels through rows and columns
    word_v_hist_proj = np.sum(thresh_img / 255, axis=0)
    word_h_hist_proj = np.sum(thresh_img / 255, axis=1) 
    # Calcualtes the value of max pixel frequency in horizontal hist projection 
    m = np.max(word_h_hist_proj)
    for row in range(thresh_img.shape[0]):
        # Creates a horizontal white line proportional size to the white pixel 
        # frequency of that row
        h_hist_img = cv2.line(
            h_hist_img, 
            (0,row), 
            (int(word_h_hist_proj[row] * w/m),row), 
            (255,255,255), 
            1)
    # Calculates the max pixel frequency value in vertical hist projection
    m = np.max(word_v_hist_proj)
    for col in range(thresh_img.shape[1]):
        # Creates a horizontal white line proportional size to the white pixel
        # frequency of that column
        v_hist_img = cv2.line(
        v_hist_img, 
        (col,h), 
        (col,h - int(word_v_hist_proj[col]*h/m)), 
        (255,255,255),
        1)
    
    return word_v_hist_proj, word_h_hist_proj, v_hist_img, h_hist_img


def segmentation_points(v_projection, block_size, step_size, thresh):
    """Algorithm that finds segmentation points in an image. Extracted from
    section 4.3 of this paper: https://www.techscience.com/cmc/v60n1/28373 

    Parameters: 
      v_projection: 1D array with the vertical hist projection values
      block_size: Size of the block to perform the sum 
      step_size: Number of steps taking in each iteration
      thresh: Minimum difference between blocks to be considered a segmentation
      point

    Returns:
      seg: Array containing all x-axis segmentation points
    """
    seg = []
    sumC = 0 # Sum of current block values
    sumP = 0 # Sum of preceding block values
    i = step_size
    j = 0
    k = 0
    while k <= block_size:
      sumP += v_projection[k]
      k += 1
    while i < (v_projection.shape[0] - block_size):
      k = i
      while k <= (i + block_size):
        sumC += v_projection[k]
        k += 1
      if (sumP - sumC) > thresh:
        # Keep the index of the segmentation
        seg.insert(j, i + (block_size / 2)) 
        j += 1
        sumP = 0
      else:
        sumP = sumC
      i += step_size
      sumC = 0

    return seg

def local_search(v_hist, seg_points, length):
    """Performs a local search around a segmentation point looking for the 
    lowest pixel frequency value.

    Parameters:
      v_hist: 1D array representing the vertical histogram projection values
      seg_points: Array containig all the x-axis segmentation points
      length: Number to determine how far to look left and right of the
      segmentation point

    Returns:
      to_ret: Array with updated segmentation points 
    """
    to_ret = []
    for seg_p in seg_points:
      start = int(seg_p - length)
      end = int(seg_p + length + 1)
      # Handle search out of bounds
      if start < 0:
        start = 0
      if end > len(v_hist):
        end = len(v_hist)
      slice_to_check = v_hist[start:end]
      # Gets the index of the lowest value of the slice and gets its true 
      # position by adding the start position
      to_ret.append(start + np.argmin(slice_to_check))
    
    return to_ret


def pixel_transition_count(thresh_img, seg_points):
    """Discard segmentation points that have more than two transitions from 
    black to white.

    Parameters:
      thresh_img: 2D array representing the thresholded image (0 or 255 values)
      seg_points: Array containing all the segmentations found
    
    Returns:
      to_ret: Array with updated segmentation points 
    """
    to_ret = []
    for seg_p in seg_points:
      # Gets the pixel values vertically from the segmentation point position
      v_slice = list(thresh_img[:,seg_p])
      changes = 0
      current = None
      for val in v_slice:
        if current == None:
          current = val
          continue
        if val != current:
          changes += 1
        current = val
      # Keep segmentaiton points that change on the vertical axis at max two times 
      if changes <= 2:
        to_ret.append(seg_p)
    
    return to_ret