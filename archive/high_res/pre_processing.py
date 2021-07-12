# Author: Joshua Soutelo Vieira
# Date: 06/01/2021

"""
This file takes single character cropped images as input. Then, some runs 
pre-processing functions them. Lastly, it outputs a CSV file containing 
the class label of that instance along with all its pixel.
"""


# Imports
import os
import csv
import argparse

import cv2
import numpy as np
from matplotlib import pyplot as plt



FILE_NAME = "Forest-characters.csv"


### Data loading function ###


def grab_images(folder):
  paths = os.listdir(folder)
  return [f"{DATA_FOLDER}/{path}" for path in paths]



### Preprocessing functions ###


# Gray scale image + Tresholding => B&W image
def bw(image, threshold=None, show=False):
  # First transform the image to gray scale
  gray_img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
  # Sometimes we choose to set the threshold manually assuming that the Otsu
  # algorithm wasn't unable to find a proper one
  if threshold:
    (thresh, bw_img) = cv2.threshold(
      gray_img,
      threshold,
      255,
      cv2.THRESH_BINARY_INV)
  else:
    # Treshold set to -0 to point out that it's Otsu's algorithm job to 
    # decide it
    (thresh, bw_img) = cv2.threshold(
      gray_img, 
      -0,
      255,
      cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  if show:
      show_image(gray_img, "Gray scale")
      show_image(bw_img, "Trehshold (B&W)")

  return bw_img


# Gaussian Blur
def gauss_blur(image, show=False):

  gauss_img = cv2.GaussianBlur(
    src=image,
    ksize=(3,3),
    sigmaX=.5)

  if show: show_image(gauss_img, "Gaussian Blur")

  return gauss_img


"""
 It coalesces rectangles until we end up with the outmost rectangle. It only takes into account rectangles that
 are at least
"""
# ROI Extraction
def roi(bw_img, gauss_img, rect_thresh=3, show=False):

  ctrs, hier = cv2.findContours(
    bw_img,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE)

  rects = [cv2.boundingRect(ctr) for ctr in ctrs]

  if len(rects) == 1: # Only one contour found
    x, y, w, h = rects[0]

  else:
    # This approach coalesces rectangles in a way that we end up 
    # with the outmost ROI
    x, y, w, h = (None, None, None, None)
    for r in rects:
      # Unpack elements
      x1, y1, w1, h1 = r
      # If the width or height of the rectangle passes a threshold
      # value
      if w1 >= rect_thresh and h1 >= rect_thresh:
        if x != None and y != None and w != None and h != None:
          # We have to take that x or y that is closer to the origin
          if x1 < x:
            x_tmp = x1
          else:
            x_tmp = x
          if y1 < y:
            y_tmp = y1
          else:
            y_tmp = y
          # We have to compute the new width and height with respect 
          # of the outer x and y
          if x1 + w1 > x + w:
            w_tmp = (x1 + w1) - x_tmp
          else:
            w_tmp = (x + w) - x_tmp
          if y1 + h1 > y + h:
            h_tmp = (y1 + h1) - y_tmp
          else:
            h_tmp = (y + h) - y_tmp
          # Update the outmost ROI
          x, y, w, h = x_tmp, y_tmp, w_tmp, h_tmp
        else:
          x, y, w, h = r
    # We didn't find a proper rectangle. Assing the one with smallest 
    # width or height so we assure that the thresholding algorithm 
    # will run again with a manual value
    if x == None and y == None and w == None and h == None:
      x, y, w, h = rects[0]
      for r in rects[1:]:
        x1, y1, w1, h1 = r
        if w1 < w or h1 < h:
          x, y, w, h = r
  """
  for r in rects:
      x1, y1, w1, h1 = r
      show_image(gauss_img[y1:y1+h1, x1:x1+w1])
  """
  roi = gauss_img[y:y+h, x:x+w]
  if show: show_image(roi, "ROI")

  return roi


def pad_resize(roi_img, show=False):
    # From EMNIST paper...
    # Extracted ROI centered in a square frame with lengths equal to 
    # the largest dimension
    h, w = roi_img.shape
    l_dim = max(h, w)
    bg_img = np.zeros((l_dim, l_dim)).astype('uint8')
    
    # Compute xoff and yoff for placement of upper left corner of 
    # resized image
    yoff = round((l_dim-h)/2)
    xoff = round((l_dim-w)/2)

    cent_img = bg_img.copy()
    cent_img[yoff:yoff+h, xoff:xoff+w] = roi_img
    if show: show_image(cent_img, "Centered")

    # Square frame padded with two empty pixels
    pad_img = cv2.copyMakeBorder(
      cent_img,
      2, 2, 2, 2, 
      cv2.BORDER_CONSTANT, 
      None,
      0)
    if show: show_image(pad_img, "Padded")

    # Downscale or upscale 
    # https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    res_img = cv2.resize(
      src=pad_img,
      dsize=(28,28),
      interpolation=cv2.INTER_CUBIC)
    if show: show_image(res_img, "Resized Image")
    
    return res_img


"""
Preprocess loop - Updated version.

If the ROI extracted is too small we run again all preprocessing steps starting from the thresholding. This time,
we set the threshold value manually, since Otsu's algorithm optimal value didn't work last time.
"""
def main():
  
  # CSV file hanlders
  csv_file = open(f"{OUTPUT_FOLDER}/{FILE_NAME}", "w")
  csvwriter = csv.writer(
    csv_file,
    delimiter=',',
    quotechar='|',
    quoting=csv.QUOTE_MINIMAL)
  
  # All cropped single character image paths
  img_paths = grab_images(DATA_FOLDER)

  for img_path in img_paths:
    img_name = img_path.split("/")[-1]
    #print(img_name)
    
    # Do pre-processing
    img = cv2.imread(img_path)
    bw_img = bw(img_path)
    gauss_img = gauss_blur(bw_img)
    roi_img = roi(bw_img, gauss_img)
    
    # Check if ROI is too small to re-run it with a manual threshold
    h, w = roi_img.shape
    if h <= 2 or w <= 2:
      bw_img = bw(img_path, threshold=150)
      gauss_img = gauss_blur(bw_img)
      
      roi_img = roi(bw_img, gauss_img)
    
    result = pad_resize(roi_img)
    
    if SAVE_PREPROCESSED_IMAGES:
      cv2.imwrite(f'{OUTPUT_FOLDER}/{img_name}',result)
    
    # Write to CSV file
    csvwriter.writerow(["None"] + result.flatten().tolist())

  csv_file.close()
  print("Preprocessing done")


if __name__ == "__main__":
  
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "input",
    help="folder containing cropped instances of single characters")
  parser.add_argument(
    "output",
    help="folder containing the pre-processing results")
  parser.add_argument(
    "--save",
    help="saves preprocessed images to output folder",
    action="store_true")

  args = parser.parse_args()
  
  # Should contain all cropped single character images
  global DATA_FOLDER 
  global OUTPUT_FOLDER
  global SAVE_PREPROCESSED_IMAGES
  
  DATA_FOLDER = args.input
  OUTPUT_FOLDER = args.output
  SAVE_PREPROCESSED_IMAGES = args.save

  main()
