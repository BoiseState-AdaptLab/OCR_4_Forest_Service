# Author: Joshua Soutelo Vieira
# Date: 06-28-2021

import json

import cv2
from PIL import Image

def grab_fields_coords(coords_json):
  """Read JSON file containing all fields coordinates."""
  with open(coords_json, "r") as f:
    content = json.loads(f.read())

  return content 

def grab_fields(form_img, coords):
  """
  Grab all the fields from a form image.
    
  Parameters
  ----------
  form_img : array
    3d-array representing the whole form image
  coords : 
    JSON file containing the coordinates of the fields

  Return
  ------
  to_ret : dict
    For each field name holds a 3d-array representing that field as an image
  """
  to_ret = {}
  fields = grab_fields_coords(coords)['fields']
  
  for field in fields:
    name = field['field']
    x = field['coord_pixel'][0]
    y = field['coord_pixel'][1]
    w = field['width']
    h = field['height']
    form_field = form_img[y:y+h, x:x+w]
    to_ret[name] = form_field

  return to_ret

# ---- word slicing functions ----
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
Iterates through the image until it finds a character. 
It explores the character to find its max_x, min_x, max_y, min_y
@return dictionary of data to populate the json file
"""
def find_char(dst, img, json_dict):
  max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
  json_list = []
  x = 0
  # Open the image using the PIL library
  im = Image.fromarray(dst)
  pixels = im.load()
  # clean the dictionary out 
  # before adding a new image
  json_dict.clear()
  #iterate through the pixels in dst
  while (x < im.size[0]): # for every pixel:
    y = 0
    while (y < im.size[1]):
      if pixels[x,y] != (0, 0, 0):
        max_x, min_x, max_y,  min_y = explore_active(x, y, im, pixels,  max_x, min_x, max_y, min_y)
        # if the area is big enough we identify it as a character
        if valid_area(max_x, max_y, min_x, min_y):
          pixels[min_x, min_y] = (255, 0 , 0)
          pixels[max_x, min_y] = (255, 0 , 0)
          pixels[min_x, max_y] = (255, 0 , 0)
          pixels[max_x, max_y] = (255, 0 , 0)
          # counter = counter + 1
          json_list.append({'x': min_x, 
                          'y': min_y, 
                          'w': max_x-min_x,
                          'h': max_y-min_y})
        y = 0
        x = max_x + 2
        if x > im.size[0]-1:
          y = im.size[1]
        max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
      else:
        y = y + 2
    x = x + 2
  #All the characters have been identified
  if valid_area(max_x, max_y, min_x, min_y):
      json_dict[img] = json_list
  
  return json_dict

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

  return max_x, min_x, max_y,  min_y

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

# ---- image preprocessing funcs ----
def convert_color_img(img, flag):
  return cv2.cvtColor(img, flag)

def blurr_img(img, kernel, flag):
  return cv2.GaussianBlur(img, kernel, flag)

def thresh_img(img, min_val, max_val, flag):
  _, thresh = cv2.threshold(img, min_val, max_val, flag)
  return thresh
# -----------------------------------

"""
Performs the image preprocessing on the field image 
before bounding boxes identification
"""
def img_preprocess(fields):
  list_of_dict = {} 

  for field in fields:
    json_dict = {}
    img = fields[field]
    #perform the image preprocessing stepss
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
    con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
    dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
    json_data = find_char(dst, field, json_dict)
    list_of_dict = dict(list_of_dict, **json_data)
  
  return list_of_dict

def word_slicing(functions, data):
  for f in functions:
    out = f(data)
    data = out
  return out
# --------------------------------

# ---- char slicing ----
def char_detection(words, fields):
  for field in fields:
    field_img = fields[field]
    show_image(field_img, f"FIELD: {field}")
    field_words = words_positions[field]
    # Find characters in each word
    char_points = []
    for field_word in field_words:
      x = field_word['x']
      y = field_word['y']
      w = field_word['w']
      h = field_word['h']
      word_img = field_img[y:y+h, x:x+w]
      # How many times does the height fits into the width?
      ratio = w / h 
      # Condition to run the slicing character approach
      if ratio > 1.5 and w > 40:
        # For each word find the characters
        gray_img = cv2.cvtColor(word_img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray_img, -0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        # Remove long horizontal lines
        res_op_1 = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, np.ones((1, 40), np.uint8))
        thresh_img -= res_op_1
        # Calculate the image vertical projection histogram
        word_v_hist_proj, word_h_hist_proj, v_hist_img, h_hist_img = create_h_v_image_proj(thresh_img)
        # Get characters
        block_size = 10
        step_size = 5
        thresh = 10
        if len(word_v_hist_proj) > block_size:
          seg_points = segmentation_points(word_v_hist_proj, block_size, step_size, thresh)
          # Improve segmentation positions
          seg_points = local_search(word_v_hist_proj, seg_points, block_size // 2)
          # Pixel transition count
          seg_points = pixel_transition_count(thresh_img, seg_points)
          # Update x coordinate in respect of original image
          char_points = char_points + [int(char_x + x) for char_x in seg_points]

# ----------------------
if __name__ == "__main__":
  # input -> fields_coords.json
  #       -> form_img 
  # output -> clean character images 
  form_img = cv2.imread("highRes_ForestService.jpg")
  fields = grab_fields(form_img, "all_fields_conservative.json")
  word_seg_functions = [
   { 'convert_color_img': [cv2.COLOR_BGR2GRAY] },
   { 'thresh_img': [0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU] },
   { 'convert_color_img': [cv2.COLOR_GRAY2BGR] },



  ]
  words = word_slicing(,fields)
  words = img_preprocess(fields)
  print(words)

