# Author: Floriana Ciaglia
# Date: January 10, 2022
# This file will contains the functions to combine the results from the JSON file produced by the pipeline
# and the JSON file produced by the Google Vision API, extract the best option and create an optimized JSON

import cv2
import json
from model.handwriting_model import run_model

def combine():
    # produce the pipeline output by running the model
    run_model() # produce the field_pred.json
    print("Pipeline model ran")

    # At this point, we have field_pred.json and google_vision_results.json
    # 1) Compare the json files
    pipeline_data, gvision_data = open_json()
    compare_data(pipeline_data, gvision_data)
    # 2) Extract the best data for each field
    # 3) Combine new results into new json file

def open_json():
    # open json files 
    pipeline = open('field_preds.json')
    gvision = open('google_vision_results.json')
 
    # returns JSON object as
    # a dictionary
    pipeline_data = json.load(pipeline)
    gvision_data = json.load(gvision)
    
    return pipeline_data, gvision_data

# def compare_data(pipeline_data, gvision_data):


    