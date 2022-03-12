# File: retrieve_Gdata.py
# Author: Floriana Ciaglia
# Date: March 12, 2022
# Description: this file retrieves data from the google vision json file and validates the 
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

def get_google_data(file_path, field_name):

    Gdata = open_file(file_path)

    for dt in Gdata:
        if dt == field_name:
            # print(field_name, ": ", Gdata[dt]['Full text']) # <-- if you want to know the accuracy percentage of the guess, 
                                                            #     print Gdata[dt]['Block confidence']
            return Gdata[dt]['Full text']



def main():
    writeup_data = get_google_data('../google_vision_results.json', 'WRITEUP NO.')
    photo_data = get_google_data('../google_vision_results.json', 'PHOTO NO.')
    forest_data = get_google_data('../google_vision_results.json', 'FOREST')
    ranger_data = get_google_data('../google_vision_results.json', 'RANGER DISTRICT')
    allotment_data = get_google_data('../google_vision_results.json', 'ALLOTMENT')
    livestock_data = get_google_data('../google_vision_results.json', 'KIND OF LIVESTOCK')


    best_match = get_most_similar_guess(livestock_data, 'KIND OF LIVESTOCK')
    print("-- Best match for livestock field ", livestock_data, "is", best_match)

    best_match = get_most_similar_guess(allotment_data, 'ALLOTMENT')
    print("-- Best match for allotment field ", allotment_data, "is", best_match)

    best_match = get_most_similar_guess(ranger_data, 'RANGER DISTRICT')
    print("-- Best match for ranger district field ", ranger_data, "is", best_match)

    best_match = get_most_similar_guess(forest_data, 'FOREST')
    print("-- Best match for forest field ", forest_data, "is", best_match)



#main function
if __name__ == '__main__':
  main()