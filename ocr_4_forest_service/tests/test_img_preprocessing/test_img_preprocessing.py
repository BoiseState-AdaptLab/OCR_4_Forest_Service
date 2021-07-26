# this file contains functions that test the image preprocessing functionality

from ...src.img_preprocessing import img_preprocessing
import os

def test_img_preprocessing():

    img_preprocessing()

    # assert that there are the same amount
    # of images in the preprocessed/ dir as 
    # in the single_chars/ dir

    count_single = 0
    count_prepro = 0
    for img in os.listdir('single_chars/'):
        count_single = count_single + 1
    
    for img in os.listdir('preprocessed/'):
        count_prepro = count_prepro + 1
    
    assert count_single == count_prepro
