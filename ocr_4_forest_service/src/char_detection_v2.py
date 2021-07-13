# Author: Joshua Soutelo Vieira
# Date: 06-28-2021

# Chain of responsability pattern https://refactoring.guru/design-patterns/chain-of-responsibility/python/example#example-0
import os
import sys
from abc import ABC, abstractmethod
import json

import cv2
import numpy as np
from PIL import Image


DIR = "fields/"
OUTPUT_FILE_NAME = "bbox_coord.json"

# ---- helper functions ----
def grab_fields_coords(coords_json):
  """Read JSON file containing all fields coordinates."""
  with open(coords_json, "r") as f:
    content = json.loads(f.read())

  return content 

def grab_fields(directory):
  try:
    return os.listdir(directory)
  except FileNotFoundError:
    print(f"FATAL ERROR. The folder {directory} was not found.")
    sys.exit(-1)
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
# --------------------------


# ---- chain of responsability interfaces ----
class Handler(ABC):
  """
  The Handler interface declares a method for building the chain of handlers.
  It also declares a method for executing a request.
  """
  @abstractmethod
  def set_next(self, handler):
    pass

  @abstractmethod
  def handle(self, request):
    pass


class AbstractHandler(Handler):
  """
  The default chaining behavior can be implemented inside a base handler
  class.
  """
  _next_handler: Handler = None
  
  def set_next(self, handler: Handler) -> Handler:
    self._next_handler = handler
    # Returning a handler from here will let us link handlers in a convenient
    # way like this: color_to_gray.set_next(threshold) 
    return handler

  @abstractmethod
  def handle(self, request):
    if self._next_handler:
      return self._next_handler.handle(request)

    return request
# --------------------------------------------


class ChangeColorImageHandler(AbstractHandler):
  """Handler implementation that changes the color of an image.
  
  Attributes:
    code: An intenger that represents the color changing operation
  """
  
  def __init__(self, code):
    self.code = code
  
  def handle(self, request):
    output = cv2.cvtColor(request, self.code)

    return super().handle(output)

   
class ThresholdImageHandler(AbstractHandler):
  """Handler implementation that performs a threshold operation to an image.
  
  Attributes:
    thresh: A number 
    maxval: 
    type:
  """
  
  def __init__(self, thresh, maxval, type):
    self.thresh = thresh
    self.maxval = maxval
    self.type = type

  def handle(self, request):
    _, output = cv2.threshold(request, self.thresh, self.maxval, self.type)
    
    return super().handle(output)


class WordDetectionHanlder(AbstractHandler):
  
  def handle(self, request):
    output = self.find_word(request)

    return super().handle(output)
  
  def find_word(self, dst):
    """
    Iterates through the image until it finds a character. 
    It explores the character to find its max_x, min_x, max_y, min_y
    @return dictionary of data to populate the json file
    """
    max_x, min_x, max_y, min_y = 0, 1000, 0, 1000
    json_list = []
    x = 0
    # Open the image using the PIL library
    im = Image.fromarray(dst)
    pixels = im.load()
    # clean the dictionary out 
    # before adding a new image
    # iterate through the pixels in dst
    while (x < im.size[0]): # for every pixel:
      y = 0
      while (y < im.size[1]):
        if pixels[x,y] != (0, 0, 0):
          max_x, min_x, max_y, min_y = self.explore_active(x, y, im, pixels, max_x, min_x, max_y, min_y)
          # if the area is big enough we identify it as a character
          if self.valid_area(max_x, max_y, min_x, min_y):
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
    if self.valid_area(max_x, max_y, min_x, min_y):
      return json_list
    else:
      return []
  
  def explore_active(self, x, y, im, pixels,  max_x, min_x, max_y, min_y):
    """
    Loops through all the pixels in the stack and colors them green when visited
    @return min and max coordinates
    """
    # Initializing a values
    stack = []
    jump_size = 1
    stack.append((x,y))

    # while the stack holds tuples
    while len(stack) != 0:
      # pop the first pair off the stack
      pair = stack.pop(len(stack)-1)
      # if the pixel is already green, we have already visited it
      if self.x_in_bound(pair[0], im) and self.y_in_bound(pair[1], im) and pixels[pair[0], pair[1]] != (0, 255, 0):
        # check and update the bbox coordinates
        max_x, min_x, max_y, min_y = self.check_coord(pair[0], pair[1], max_x, min_x, max_y, min_y)
        # check to the right
        if self.look(pair[0]+jump_size, pair[1], im, pixels):
          stack.append((pair[0]+jump_size,pair[1]))
        # check down-wards
        if self.look(pair[0], pair[1]+jump_size, im, pixels):
          stack.append((pair[0],pair[1]+jump_size))
        # check to the left 
        if self.look(pair[0]-jump_size, pair[1], im, pixels):
          stack.append((pair[0]-jump_size,pair[1])) 
        # check up-wards
        if self.look(pair[0], pair[1]-jump_size, im, pixels):
          stack.append((pair[0],pair[1]-jump_size)) 
        #turn the pixel green to sign it as visited
        pixels[pair[0], pair[1]] = (0, 255, 0)

    return max_x, min_x, max_y,  min_y
  
  def x_in_bound(self, x, im):
    """
    Checks the x axis boundary
    @return boolean
    """    
    if x >= 0 and x <= im.size[0]-1:
      return True
    else:
      return False

  def y_in_bound(self, y, im):
    """
    Checks the y axis boundary
    @return boolean
    """
    if y >= 0 and y <= im.size[1]-1:
      return True
    else:
      return False
  
  def check_coord(self, x, y, max_x, min_x, max_y, min_y):
    """
    Updates the max and min coordinates
    """
    if x > max_x:
      max_x = x
    if x < min_x:
      min_x = x
    if y > max_y:
      max_y = y
    if y < min_y:
      min_y = y

    return max_x, min_x, max_y,  min_y

  def look(self, x, y, im, pixels):
    """
    Looks if the neighbor pixels is available
    """
    retVal = False
    # check if x and y are in bound
    if self.x_in_bound(x, im) and self.y_in_bound(y, im):
      if pixels[x, y] != (0, 0, 0):
        retVal = True

    return retVal

  def valid_area(self, max_x, max_y, min_x, min_y):
    """
    Accepts only the areas that are bigger than 100
    @return boolean
    """
    # calculate the area of the bbox to 
    # minimize noise
    width = max_x - min_x
    height = max_y - min_y
    area = width * height
    if area > 100:
      return True
    else:
      return False

class CharacterDetectionHandler(AbstractHandler):

  def __init__(self, ratio_constrain, width_constrain, block_size, step_size, thresh):
    self.ratio_constrain = ratio_constrain
    self.width_constrain = width_constrain
    self.block_size = block_size
    self.step_size = step_size
    self.thresh = thresh
  
  def handle(self, request):
    output = self.find_char(request)

    return super().handle(output)

  def find_char(self, request):
    letters, field_img = request
    char_points = []
    for field_word in letters:
      x = field_word['x']
      y = field_word['y']
      w = field_word['w']
      h = field_word['h']
      word_img = field_img[y:y+h, x:x+w]
      # How many times does the height fits into the width?
      ratio = w / h 
      # Condition to run the slicing character approach
      if ratio > self.ratio_constrain and w > self.width_constrain:
        # For each word find the characters
        gray_img = cv2.cvtColor(word_img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(gray_img, -0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        # Remove long horizontal lines
        res_op_1 = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, np.ones((1, 40), np.uint8))
        thresh_img -= res_op_1
        # Calculate the image vertical projection histogram
        word_v_hist_proj, word_h_hist_proj, v_hist_img, h_hist_img = self.create_h_v_image_proj(thresh_img)
        # Get characters
        if len(word_v_hist_proj) > self.block_size:
          seg_points = self.segmentation_points(word_v_hist_proj, self.block_size, self.step_size, self.thresh)
          # Improve segmentation positions
          seg_points = self.local_search(word_v_hist_proj, seg_points, self.block_size // 2)
          # Pixel transition count
          seg_points = self.pixel_transition_count(thresh_img, seg_points)
          seg_points = [int(char_x + x) for char_x in seg_points]
          # Update x coordinate in respect of original image
          if seg_points != []:
            char_points.append({"orig_coords": field_word, "char_coords": seg_points})
          else:
            char_points.append(field_word)
      else:
        char_points.append(field_word)

    # From segmentation lines to actual x, y, w, and h inside the field
    bbox_coords = []
    for chars in char_points:
      if "orig_coords" in chars.keys():
        orig_x = chars['orig_coords']['x']
        orig_y = chars['orig_coords']['y']
        orig_h = chars['orig_coords']['h']
        orig_w = chars['orig_coords']['w']
        
        prev_seg_line = orig_x
        seg_lines = chars['char_coords']
        for seg_line in seg_lines:
          x = prev_seg_line
          w = seg_line - prev_seg_line
          y = orig_y
          h = orig_h
          bbox_coords.append({"x": x, "y": y, "w": w, "h": h})
          prev_seg_line = x + w
        # Append the last one
        w = (orig_x + orig_w) - (x + w)
        bbox_coords.append({"x": prev_seg_line, "y": y, "w": w, "h": h})
      else:
        bbox_coords.append(chars)
    
    # Remove single pixel width characters (small enough to be a character) 
    for coord in bbox_coords:
      w = coord['w']
      h = coord['h']
      if w <= 2 or h <= 2:
        bbox_coords.remove(coord)
        
    return bbox_coords

  def create_h_v_image_proj(self, thresh_img):
    h, w = thresh_img.shape[:2]
    h_hist_img = np.zeros(thresh_img.shape[:2], dtype='uint8')
    v_hist_img = np.zeros(thresh_img.shape[:2], dtype='uint8')

    word_v_hist_proj = np.sum(thresh_img / 255, axis=0)
    word_h_hist_proj = np.sum(thresh_img / 255, axis=1) 

    m = np.max(word_h_hist_proj)
    for row in range(thresh_img.shape[0]):
      h_hist_img = cv2.line(
        h_hist_img, 
        (0,row), 
        (int(word_h_hist_proj[row] * w/m),row), 
        (255,255,255), 
        1)
    m = np.max(word_v_hist_proj)
    for col in range(thresh_img.shape[1]):
      v_hist_img = cv2.line(
      v_hist_img, 
      (col,h), 
      (col,h - int(word_v_hist_proj[col]*h/m)), 
      (255,255,255),
      1)
    return word_v_hist_proj, word_h_hist_proj, v_hist_img, h_hist_img
    
  def segmentation_points(self, v_projection, block_size, step_size, thresh):
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

  def local_search(self, v_hist, seg_points, length):
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
      to_ret.append(start + np.argmin(slice_to_check))
    return to_ret

  def pixel_transition_count(self, thresh_img, seg_points):
    to_ret = []
    for seg_p in seg_points:
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
      if changes <= 2:
        to_ret.append(seg_p)
    return to_ret


def word_pipeline(fields, handler: Handler):
  words = {}
  for field_name in fields:
    field_img = cv2.imread(DIR + field_name)
    output = handler.handle(field_img)
    words[field_name] = output
  return words 

def char_pipeline(fields, words, handler: Handler):
  chars = {}
  for field_name in fields:
    letters = words[field_name]
    field_img = cv2.imread(DIR + field_name)
    output = handler.handle((letters, field_img))
    chars[field_name] = output
  return chars

 
def create_json(list_of_dict):
  """
  Creates the json file with the bbox coordinates
  """
  
  # store the data into a new json file
  with open(OUTPUT_FILE_NAME, 'a') as outfile: 
    json.dump(list_of_dict, outfile)


def main():
  # Data that both pipelines will use
  fields = grab_fields(DIR)
  
  # Defines the word extracting pipeline
  color_to_gray = ChangeColorImageHandler(code=cv2.COLOR_BGR2GRAY)
  threshold = ThresholdImageHandler(0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  gray_to_color = ChangeColorImageHandler(code=cv2.COLOR_GRAY2BGR)
  word_detector = WordDetectionHanlder() 
  # Builds word extracting pipeline 
  color_to_gray.set_next(threshold).set_next(gray_to_color).set_next(word_detector)
  # Executes word extracting pipeline 
  words = word_pipeline(fields, color_to_gray)
  
  # Defines the character extracting pipeline
  char_detector = CharacterDetectionHandler(ratio_constrain=1.5, width_constrain=40, block_size=10, step_size=5, thresh=10)
  # Executes character extracting pipeline
  chars = char_pipeline(fields, words, char_detector)
  
  # Saves the coordiantes to a JSON file
  create_json([chars])
    
# ----------------------
if __name__ == "__main__":
  main()

