# File: retrieve_Pdata.py
# Author: Floriana Ciaglia
# Date: March 15, 2022
# Description: this file retrieves data from the pipeline json file and validates the 
#              FOREST, ALLOTMENT, KIND OF LIVESTOCK and REANGER DISTRICT fields with the db tables. 

import json
import sys
from os import path
from crop_bbox import open_json

sys.path.append(path.abspath('/home/FLOCIAGLIA/ForestryServiceDatabase/db/orm_scripts'))
from pipe_get_data import get_most_similar_guess

def open_file(file_name):
    # Opening JSON file
    f = open(file_name)
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    return data


def get_data(file_path, field_name):

    data = open_file(file_path)

    for dt in data:
        if dt == field_name:
            # print(field_name, ": ", Gdata[dt]['Full text']) # <-- if you want to know the accuracy percentage of the guess, 
                                                            #     print Gdata[dt]['Block confidence']
            guess_list =  data[dt]['Full text']
    
    return create_word(guess_list)

def create_word(guess_list):
    word = ''

    for letter in guess_list:
        word += letter
    
    return word.lower()



def get_writeup(file_path):
    return get_data(file_path, 'WRITEUP NO.')

def get_photo(file_path):
    return get_data(file_path, 'PHOTO NO.')

def get_forest(file_path):
    forest_data = get_data(file_path, 'FOREST')
    return get_most_similar_guess(forest_data, 'FOREST')

def get_ranger_dist(file_path):
    ranger_data = get_data(file_path, 'RANGER DISTRICT')
    return get_most_similar_guess(ranger_data, 'RANGER DISTRICT')

def get_allotment(file_path):
    allotment_data = get_data(file_path, 'ALLOTMENT')
    return get_most_similar_guess(allotment_data, 'ALLOTMENT')

def get_examiner(file_path):
    return get_data(file_path, 'EXAMINER')

def get_date(file_path):
    return get_data(file_path, 'DATE')

def get_livestock(file_path):
    livestock_data =  get_data(file_path, 'KIND OF LIVESTOCK')
    return get_most_similar_guess(livestock_data, 'KIND OF LIVESTOCK')

def get_transect(file_path):
    return get_data(file_path, 'TRANSECT NO.')

def get_plot_size(file_path):
    return get_data(file_path, 'PLOT SIZE')

def get_plot_inter(file_path):
    return get_data(file_path, 'PLOT INTERVAL')

def get_type_des(file_path):
    return get_data(file_path, 'TYPE DESIGNATION')

def get_type_des(file_path):
    return get_data(file_path, 'TYPE DESIGNATION')

def get_slope(file_path):
    return get_data(file_path, 'SLOPE')

def get_aspect(file_path):
    return get_data(file_path, 'ASPECT')

def get_exposure(file_path):
    return get_data(file_path, 'EXPOSURE')

def get_location(file_path):
    return get_data(file_path, 'LOCATION')

def get_elevation(file_path):
    return get_data(file_path, 'ELEVATION')

def report_data(file_path):

    return (get_writeup(file_path), get_photo(file_path), get_forest(file_path), get_ranger_dist(file_path),
    get_allotment(file_path), get_examiner(file_path), get_date(file_path), get_transect(file_path), get_plot_size(file_path),
    get_plot_inter(file_path), get_type_des(file_path), get_livestock(file_path), get_slope(file_path), get_exposure(file_path), 
    get_location(file_path), get_elevation(file_path))



# print(get_forest('../field_preds.json'))