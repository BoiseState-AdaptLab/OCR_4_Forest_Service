# Author: Joshua Soutelo Vieira
# Date: 06-28-2021

from abc import ABC, abstractmethod
import json

import cv2
from PIL import Image


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
    # way like this: 
    return handler

  @abstractmethod
  def handle(self, request):
    if self._next_handler:
      return self._next_handler.handle(request)

    return request


# ---- handler implementations ----
class ChangeColorImageHandler(AbstractHandler):
  
  def __init__(self, code):
    self.code = code
  
  def handle(self, request):
    output = cv2.cvtColor(request, self.code)

    return super().handle(output)

   
class ThresholdImageHandler(AbstractHandler):
  
  def __init__(self, thresh, maxval, type):
    self.thresh = thresh
    self.maxval = maxval
    self.type = type

  def handle(self, request):
    _, output = cv2.threshold(request, self.thresh, self.maxval, self.type)
    
    return super().handle(output)


class WordDetectionHanlder(AbstractHandler):
  
  def handle(self, request):
    output = self.find_char(request)

    return super().handle(output)
  
  def find_char(self, dst):
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
    #iterate through the pixels in dst
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
  
  def handle(self, request):
    f_name, f_img = request
    output = cv2.cvtColor(f_img, self.code)

    return super().handle((f_name, output))


# ---------------------------------
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

def word_pipeline(handler: Handler):
  words = {}
  form_img = cv2.imread("highRes_ForestService.jpg")
  fields = grab_fields(form_img, "all_fields_conservative.json")
  for field_name, field_img in fields.items():
    output = handler.handle(field_img)
    words[field_name] = output
    ##cv2.imshow(field_name, output)
    ##cv2.waitKey(0) # waits until a key is pressed
    ##cv2.destroyAllWindows() # destroys the window showing image
  return words 
# ----------------------
if __name__ == "__main__":
  # input -> fields_coords.json
  #       -> form_img 
  # output -> clean character images 

  # Defines the word extracting pipeline
  color_to_gray = ChangeColorImageHandler(code=cv2.COLOR_BGR2GRAY)
  threshold = ThresholdImageHandler(0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  gray_to_color = ChangeColorImageHandler(code=cv2.COLOR_GRAY2BGR)
  word_detector = WordDetectionHanlder() 

  color_to_gray.set_next(threshold).set_next(gray_to_color).set_next(word_detector)
  words = word_pipeline(color_to_gray)
  print(words)
  # Defines the character extracting pipeline

  #change_color_image = (cv2.COLOR_BGR2GRAY)
  

