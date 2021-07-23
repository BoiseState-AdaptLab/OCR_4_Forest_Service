# This file contains the functions that test the character detection functionality

from ..src.char_detection import char_detection
from ..src.crop_bbox import output_dir
from ..src.crop_bbox import crop
import json
import os

def test_char_dect_overall():

    char_detection()
    output_dir()

    json_file = open('bbox_coord.json')
    fields = json.load(json_file)

    crop(fields)

    DIR = 'single_chars/'

    i = 0
    for img in os.listdir(DIR):
        i = i + 1

    assert i == 112 
