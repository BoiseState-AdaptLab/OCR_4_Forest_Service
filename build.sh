#!/bin/bash

. venv/bin/activate

# This command will run the pipeline with the inputs provided
python3 ocr_4_forest_service/ocr_4_forest_service.py -i ocr_4_forest_service/inputs/forms/site_an_sum_25.jpeg -json ocr_4_forest_service/inputs/jsons/template2.json -temp ocr_4_forest_service/inputs/forms/template2.jpg -p

if [ $? -eq 0 ] 
then 
  printf "Code executed successfully.\n" 
else 
  printf "Code exited with error.\n"
fi

deactivate