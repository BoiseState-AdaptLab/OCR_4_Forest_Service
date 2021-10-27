# this file contains tests for the image enhancement
import cv2
import numpy as np
from ...src.char_detection import img_preprocess
from ...src.char_detection import line_deletion
from ...src.char_detection import trace
from ...src.char_detection import word_segmentation
from ...src.char_detection import word_seg_2

import numpy as np
import glob
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import skimage.io
import skimage.color
import skimage.filters


def test_preprocessing_techniques():

    # imgs = cv2.imread('../../21-cropped_fields/WRITEUP NO..jpg', 1)
    # img_preprocess(imgs)

    img = cv2.imread('../../cropped_fields/ALLOTMENT.jpg', 1)
    # con_img = local_preprocesssing(img)
    con_img = img_preprocess(img)

   
    # plot_preprocessed(con_img)
    
    con_img = line_deletion(con_img)
    cv2.imshow(f'after line deletion', con_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    single_char_list = trace(con_img)
    print("length of list: ", len(single_char_list))
    word_segmentation_list = []
    word_seg_list = []

    for image in single_char_list:
        
        sliced_images = word_segmentation(image, 'KIND OF LIVESTOCK')
        print("sliced images:", type(sliced_images[0][0]))

        cv2.imshow('sliced img', sliced_images[0][0])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if sliced_images is None:
          # print("for one of them we get in here")
          break
        else:

          for img in sliced_images:
            cv2.imshow('img', img[0])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imshow('Word segmentation 1', img[0])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            segmented_imgs = word_seg_2(img[0])
            # print("segmented images", len(segmented_imgs))
          

            word_seg_list.extend(segmented_imgs)
        for img in word_seg_list:
          print(type(img))
          cv2.imshow('returned', img)
          cv2.waitKey(0)
          cv2.destroyAllWindows()
        print("chars list: ", len(word_seg_list))
        word_segmentation_list = [(x,'KIND OF LIVESTOCK') for x in word_seg_list]
      # print("segmented images",  type(word_segmentation_list[0][0]))
     
      # word_segmentation_list.extend(sliced_images)
    assert 1 == 0
  
     
  
    return word_segmentation_list



def plot_preprocessed(con_img):
    print("inside this function")
    histogram = cv2.calcHist([con_img], [0], None, [256], [0, 256])
    plt.plot(histogram, color='k')
    plt.show()

    # matplotlib expects RGB images so convert and then display the image
    # with matplotlib
    # plt.figure()
    # plt.axis("off")
    # plt.imshow(cv2.cvtColor(con_img, cv2.COLOR_GRAY2RGB))
    # # plot the histogram
    # plt.figure()
    # plt.title("Grayscale Histogram")
    # plt.xlabel("Bins")
    # plt.ylabel("# of Pixels")
    # plt.plot(histogram)
    # plt.xlim([0, 256])

    
def local_preprocesssing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # dst = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)


    histogram = cv2.calcHist([img], [0], None, [256], [0, 256])
    plt.plot(histogram, color='k')
    plt.show()
  
    
    t = find_thresh(histogram)
    print("the thresh value chosen is", t)
 
    # Thresholding with threshold value set t
    th, dst = cv2.threshold(img,t,255, cv2.THRESH_BINARY_INV)

    cv2.imshow(f'thresh', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    con_img = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    return con_img
   



def find_thresh(histogram):

    # cast historgram to numpy array
    # histogram = np.array(histogram)

    # Find the peak in the histogram
    peak =  int(max(histogram))

    # Get the index of peak
    peak_idx = np.where(histogram == peak)

    # peak_idx is a tuple of numpy arrays
    # So, we need to index into the first 
    # element of the tuple, and then into
    # the first element of the array ([0][0])
    histogram = histogram[:peak_idx[0][0]+1]

    # start froom the peak and go backwards
    for item in reversed(histogram):
        if item[0] < 50: # 50 seems like a good threshold
            # break as soon as we get a value below 50
            # print("first to get hit", item[0])
            y_val = item[0]
            break
    
    # find the index of just found value
    y_idx = np.where(histogram == y_val)

    # again, where() returns a tuple of
    # np arrays, so we need to index them.
    if len(y_idx[0]) > 1:
        t_val = y_idx[0][-1]
    else:
       
        t_val = y_idx[0][0] 

    return t_val




def find_thresh_2(histogram):

    lenght = len(histogram)
    thresh = []
    for val in range(lenght-10):
   
        diff = int(histogram[val+10][0]) - int(histogram[val][0])
   
        if diff != 0:
            thresh.append({'x': val, 'y': val+10, 'diff': diff})

    max_diff = 0
    for t in thresh:
        if t['diff'] > max_diff:
            max_diff = t['diff']
    
    print("max_diff", max_diff)
    t_val = 0
    for t in thresh:
        if t['diff'] == max_diff:
            t_val = t['x']
            print(t['x'], t['y'])
            
    return t_val



def img_preprocess(img):

    # perform the image preprocessing stepss
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    cv2.imshow(f'IMG_PREPROCESSING', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
    return con_img
    
def img_enhancement(img):
    print("inside enhancement")
    # perform the image preprocessing stepss
    # 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.THRESH_BINARY_INV+

    global_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 111, 0)
    # cv2.imshow(f'threshold', global_thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
   
    con_img = cv2.cvtColor(global_thresh, cv2.COLOR_GRAY2BGR)
 
    return con_img


# def edge_connection():


def noise_reduction(img):
    
    return cv2.bilateralFilter(img,9,75,75)


