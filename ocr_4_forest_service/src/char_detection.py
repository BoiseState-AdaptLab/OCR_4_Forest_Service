# Author: Floriana Ciaglia, Joshua Suotelo Vieira
# Date: May 14th, 2021

# This program creates a bounding box around a discrete letter by:
#       - taking a field image as an input
#       - iterating through each pixel in the image
#       - keeping track of max x, max y, min x, min y

import cv2
from os import path
from PIL import Image
from queue import LifoQueue
import numpy as np
import math

"""
Definition of the main fuction
"""
def char_detection(field_img, field_name): # char_detection takes in a list of field images
  
      
    # cv2.imshow('livestock', field_img)
    # # cv2.imwrite("field_img.jpg", field_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # word_segmentation_list = []
    # if field_name == "WRITEUP NO.":
    con_img = img_preprocess(field_img)

    # cv2.imshow('preprocessed', con_img)
    # # cv2.imwrite("field_img.jpg", field_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    con_img = line_deletion(con_img)
  

    # lines 48-54 need commenting out
    # cv2.imshow('line detection', con_img)
    # # cv2.imwrite("field_img.jpg", field_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # exit()
    single_char_list = trace(con_img)

    # print("single char list for writeup no:", len(single_char_list))

    word_segmentation_list = []
    word_seg_list = []

    for image in single_char_list:
        
        sliced_images = word_segmentation(image, field_name)
        # print("sliced images:", type(sliced_images[0][0]))

        # cv2.imshow('img', sliced_images[0][0])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if sliced_images is None:
          # print("for one of them we get in here")
          break
        else:

          for img in sliced_images:
            # cv2.imshow('img', img[0])
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # cv2.imshow('Word segmentation 1', img[0])
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            segmented_imgs = word_seg_2(img[0])
            # print("segmented images", len(segmented_imgs))
          

            word_seg_list.extend(segmented_imgs)
        # for img in word_seg_list:
        #   print(type(img))
        #   # cv2.imshow('returned', img)
        #   # cv2.waitKey(0)
        #   # cv2.destroyAllWindows()
        # print("chars list: ", len(word_seg_list))
        word_segmentation_list = [(x,field_name) for x in word_seg_list]
      # print("segmented images",  type(word_segmentation_list[0][0]))
     
      # word_segmentation_list.extend(sliced_images)
  
     
  
    return word_segmentation_list

   
# @param: image object
# @return: list of image objects
# This function takes in an image 
# objects, performs character detection 
# on the image, saves the tracing and 
# creates the another image with the 
# trace of the letter.  
def trace(image):
    """
    Get all traces beloging to the characters of the image.
    """
    dict_bbox_coord, tracing_data = find_char(image)
    
    list_images = single_chars(dict_bbox_coord, tracing_data)
    
    return list_images


def line_deletion(con_img):
    """
     This function removes the bottom line 
     in each field-it removes noise factors.
    """
   
    white = 5
  
    # from numpy array to PIL
    img = Image.fromarray(con_img)
    pixels = img.load() # create the pixel map
          
    y_coord = int(img.size[1])
    for x in range(img.size[0]):
        for y in range(y_coord - 2, y_coord):
            if pixels[x,y] == (255, 255, 255):
                white += 1
                if white > 5:
                    #img.putpixel((x,y),(255, 0, 0))
                    img.putpixel((x,y), (0, 0, 0))
            else:
                white == 0



    # from PIL to numpy array
    img = np.array(img)
    return img

# @param: dictionary with bounding box coordinates and 
# the dictionary with the tracing data 
# @return: a list of image objects for each bbox in the field 
# This function creates a brand new image and pastes the 
# tracing of the characters on it in order to remove noise. 
def single_chars(dict_bbox_coord, tracing_data):

    # this is the data structure that holds
    # all the single char image objects to return
    single_chars_list = []

    for box in dict_bbox_coord:
        box_name = box['box']
        traces = tracing_data[box_name]
        
        blank_image = np.zeros((box['h'],box['w']), np.uint8)
        blank_image[:] = 255
    
        for x, y in traces:
            # we need to subtract the original field x coordinate
            # from the bbox to align the coordinates of the bbox
            tuple = (x-box['x'], y-box['y'])
        
            blank_image[tuple[1]][tuple[0]] = 0

        single_chars_list.append(blank_image)

    return single_chars_list


"""
Performs the image preprocessing on the field image 
before bounding boxes identification
"""
def img_preprocess(img):

    # perform the image preprocessing stepss
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
 
    return con_img
    
    


def find_char(preprocessed_field_img):
    """
    Iterates through the image until it finds a character. 
    It explores the character to find its max_x, min_x, max_y, min_y
    @return dictionary of data to populate the json file
    """

    json_list = []
    tracing_list = {}
    tracing = []

    max_x, min_x  = 0, 1000, 
    max_y, min_y = 0, 1000
    
    x = 0

    # Open the image using the PIL library
    im = Image.fromarray(preprocessed_field_img)
    pixels = im.load()

    # clean the dictionary out 
    # before adding a new image

    i = 0
    #iterate through the pixels in dst
    while (x < im.size[0]): # for every pixel:
        y = 0
        
        while (y < im.size[1]):
            
            #if the pixel is white
            if pixels[x,y] != (0, 0, 0):
                
                max_x, min_x, max_y,  min_y, traces = explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y)
                # print("##traces: ", trace)
                # if the area is big enough we identify it as a character
                if valid_area(max_x, max_y, min_x, min_y):
                    pixels[min_x, min_y] = (255, 0, 0)
                    pixels[max_x, min_y] = (255, 0, 0)
                    pixels[min_x, max_y] = (255, 0, 0)
                    pixels[max_x, max_y] = (255, 0, 0)

                    # show the image get colored at every bbox found
                    # im.show()

                    box_num = 'box_{num}'.format(num = i)
                    # 
                    json_list.append({'box': box_num,
                                    'x': min_x, 
                                    'y': min_y, 
                                    'w': max_x-min_x,
                                    'h': max_y-min_y})

                    # im.show()
                    
                    tracing = get_tracing(pixels, box_num, tracing, max_x, min_x, max_y, min_y, traces)
       
                    tracing_list.update(**tracing)
                    
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

    return json_list, tracing_list
 


def word_seg_2(sliced_img): # single segmented image coming from the first word segmentation technique
 
    new_char_list = []

    # 1) turn image to binary threshold
    _, thresh = cv2.threshold(sliced_img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # cv2.imshow('Original', sliced_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    height, width = sliced_img.shape
    # print("height, width:", height, width)

    if height == 0 or width == 0 :
      return new_char_list

    # 2) create vertical histogram projection
    vertical_hist = np.sum(thresh, axis=0, keepdims=True)/255

    # creare a blank image for vertical histogram
    blank_img = np.zeros([height,width,3],dtype=np.uint8)
    blank_img[:] = 255

    total = 0
    # visual representation of vertical histogram
    for i, num in enumerate(vertical_hist[0]):
        total += num
        cv2.line(blank_img, pt1=(i,height), pt2=(i,height-int(num)), color=(0,0,0), thickness=1)

    # cv2.imshow('Vertical Histogram', blank_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # implement the word-segmentation lining on the image
    seg_points = []
    copy_lines = sliced_img.copy()
    for i, num in enumerate(vertical_hist[0]):
        if num < (total*.01):
            cv2.line(copy_lines, pt1=(i,height), pt2=(i,0), color=(0,0,0), thickness=1)
            seg_points.append((i, height))
    # print(seg_points)

    # cv2.imshow('image with seg lines', copy_lines)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
   
    if len(seg_points) < 1:
        # print("We DON'T have lines")
        # print("adding to list")
        new_char_list.append(sliced_img)
        # cv2.imshow('returned', sliced_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # return sliced_img
    # we found segmentation lines in the image. So, we have some logic in here:
    #    1) The lines are either at the very front or very back of the image --> disregard them
    #    2) The lines divide two letters --> create the two distinct images 

    else:
        # print("We DO have lines")
        # print("seg points:", seg_points)
        # start_x = 0
        start_y = 0
        end_x = 0

        copy = sliced_img.copy()
        
        for seg_point in seg_points:
            # curr_seg_point = seg_point
            # create a copy of the original image
            start_x = end_x
            end_x = seg_point[0]
            end_y = seg_point[1]
            # print("- left threshold:", width*.1)

            # if the segment is in bound
            if end_x > 3 and end_x < width-2:
                # print("we don't get in here for 2")
                # if the segment is wider than 3 pixels
                if (end_x - start_x) > 3:
                    # print("start_x", start_x)
                    # print("start_y", start_y)
                    # print("end_x", end_x)
                    # print("end_y", end_y)
                    
                    #image[start_x:end_x, start_y:end_y]
                    # cropped = copy.crop((start_x, 0, end_x, height))
                    # images.append(cropped)
                    # print("adding to list")
                    new_char_list.append(copy[start_y:end_y, start_x:end_x])
                    # print("It's happening here...")
                    # cv2.imshow('# segmenting 2', copy[start_y:end_y, start_x:end_x])
                    # # cv2.imshow('## segmenting', image[start_x:end_x,start_y:end_y])
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()

                    
              # start_y = end_y
            # prev_seg_point = curr_seg_point
        
        # print("width", width)
        # print("height", height)
        # print("#######################")
        # print("start_x", start_x)
        # print("start_y", start_y)
        # print("end_x", end_x)
        # print("end_y", end_y)

        # This covers the case where the segmentation lines are at the 
        # beginnig of the image before the character
        if end_x < 3:
          # print("Do we ever get in here? ")
          # print("Weird case")
          # print("adding to list")
          new_char_list.append(sliced_img)
          # cv2.imshow('# segmenting 2', sliced_img)
          # # cv2.imshow('## segmenting', image[start_x:end_x,start_y:end_y])
          # cv2.waitKey(0)
          # cv2.destroyAllWindows()

        elif (width - end_x) > 5 :
          # print("adding to list in the forth place")
          new_char_list.append(copy[start_y:end_y, end_x:width-1])
          # print("height of segment:", end_y-start_y)
          # cv2.imshow('## segmenting 2', copy[start_y:end_y, end_x:width-1])
          # cv2.waitKey(0)
          # cv2.destroyAllWindows()
        elif ((end_x - start_x) < 3) and width - end_x < 3:
          # print("2 should be added heree")
          new_char_list.append(copy[start_y:end_y, 0:start_x])

        elif (end_x > 1 and end_x < width) and ((end_x - start_x) > 3):
          # print("adding to list in the third place")
          new_char_list.append(copy[start_y:end_y, start_x:end_x])
          # # print("height of segment:", end_y-start_y)
          # cv2.imshow('## segmenting 2', copy[start_y:end_y, start_x:end_x])
          # cv2.waitKey(0)
          # cv2.destroyAllWindows()
          # cv2.imwrite('segment.jpg', copy[start_y:end_y, start_x:end_x])
          # segment = cv2.imread('segment.jpg')
          # print(segment.shape)
          # print("len images", len(images))

        


    # new_char_list.append(images)
    # print("len list", len(new_char_list))

    # for image in new_char_list:
      # print("Ricapitolando...")
      # # print(image[0].shape)
      # img = Image.fromarray(image)
      # # print(img.shape())
      # # img.save('test.png')
      # img.show()

    return new_char_list


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
        # print("## Error: The area was ", area)
        return False



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
    trace = []
    
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
            trace.append((pair[0], pair[1]))

    # 
    # im.show()
    
    return max_x, min_x, max_y,  min_y, trace


def get_tracing(pixels, box_num, tracing, max_x, min_x, max_y, min_y, traces):
    tracing_dict = {}
    tracing = []
  
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            
            if pixels[x, y] == (0,  255, 0) and (x, y) in set(traces):
                tracing.append((x,y))
    tracing_dict[box_num] = tracing
    
    # We now have the entire tracing of the character
    return tracing_dict



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
    # print("word hist:", word_h_hist_proj )
    # Calcualtes the value of max pixel frequency in horizontal hist projection 
    m = np.max(word_h_hist_proj)
    # print("max:", m)
    if m == 0:
      return -1
    
    for row in range(thresh_img.shape[0]):
        # Creates a horizontal white line proportional size to the white pixel 
        # frequency of that row
        # print("m: ", m, "w:", w, "longer thing:", word_h_hist_proj[row])
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
    
    return word_v_hist_proj


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



def word_segmentation(image, field_name):

    h, w = image.shape[:2]
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
        _, thresh_img = cv2.threshold(image, -0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
     
        # Remove long horizontal lines
        res_op_1 = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, np.ones((1, 40), np.uint8))
        thresh_img -= res_op_1

        # Calculate the image vertical projection histogram
        word_v_hist_proj = create_h_v_image_proj(thresh_img)
        # print(word_v_hist_proj)
        if type(word_v_hist_proj) == int:
            return

        # Get characters
        if len(word_v_hist_proj) > block_size:
            seg_points = segmentation_points(word_v_hist_proj, block_size, step_size, thresh)
            # Improve segmentation positions
            seg_points = local_search(word_v_hist_proj, seg_points, block_size // 2)
            # Pixel transition count
            seg_points = pixel_transition_count(thresh_img, seg_points)
            # print("type of seg points: ", type(seg_points))
            # print(seg_points)
            prev_seg_point = 0
            curr_seg_point = 0
            images = []
            for seg_point in seg_points:
                curr_seg_point = seg_point
                images.append((image[:,prev_seg_point:curr_seg_point], field_name))
                prev_seg_point = curr_seg_point
            images.append((image[:,curr_seg_point:image.shape[1] - 1], field_name))
  
            return images
            
    else:

        return [(image, field_name)]
