# file: create_report.py
# desc: this file gets the data from the pipeline repo and creates an insert statement to insert the data into the db. 

import json
import sys
import os
from os import path

sys.path.append(path.abspath('/home/kdoster/OCR_4_Forest_Service/ocr_4_forest_service/src/'))
from retrieve_data import report_data

def create_insert_statement():
  # change the path to the file if you want results form google vision [google_vision_results.json] or pipeline [field_preds.json]
  # ../OCR_4_Forest_Service/ocr_4_forest_service/
  what = report_data('field_preds.json')
  
  print("******** This is string", what, "\n")  
  string = "insert into report (writeup_no, photo_no, forest, ranger_district, allotment, examiner, date, transect_no, plot_size, plot_interval, type_designation, livestock, slope, aspect, location, elevation) values (" + "'" + what[0] + "'" + ","  + "'" +what[1] + "'" + "," + "'" + what[2] + "'" + "," + "'" + what[3] + "'" + "," + "'" +what[4] + "'"+ "," + "'" +what[5]+ "'" + "," + "'" +what[6] + "'"+ "," + "'" +what[7]+ "'" + "," + "'" +what[8] + "'"+ "," + "'" +what[9]+ "'" + "," + "'" +what[10] + "'"+ "," + "'" +what[11] + "'"+ "," + "'" +what[12] + "'"+ "," + "'" +what[13] + "'"+ "," + "'" +what[14]+ "'" + "," + "'" +what[15] + "'"+ ")"
  # print("******** This is string", string, "\n")
  with open(os.path.join('queries/', "insert_report.txt"), "w") as text_file:
    text_file.write(string)
    text_file.close()


#main function
if __name__ == '__main__':
  create_insert_statement()
