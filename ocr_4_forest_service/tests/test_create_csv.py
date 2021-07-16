# this file contains the functions that test the create_csv functionality

from ..src.create_csv import create_csv
import os
import csv

def test_create_csv():

    create_csv()

    # count how many lines the csv file has
    # and assert that they match with the 
    # amount of images stored in preprocessed/

    file = open("test_data.csv")
    reader = csv.reader(file)
    lines= len(list(reader))

    count = 0
    for img in os.listdir('preprocessed/'):
        count = count + 1
    
    assert count == lines
