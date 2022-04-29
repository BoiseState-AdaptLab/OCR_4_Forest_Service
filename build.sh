#!/bin/bash

. forest_env/bin/activate

while getopts i:v:n: opt; 
do
    case ${opt} in
        # Input file name
        i) input=${OPTARG};;
        # run the production pipeline
        v)  version=${OPTARG};;
        # template number
        n)  number=${OPTARG};;

        \?) # Invalid option
            echo "Error: You entered an invalid flag."
            exit 1;;
    esac
done


# This command will run the pipeline with the inputs provided
if [[ "$version" == "pipeline" ]];
then   
    echo "---- You chose to run the pipeline."
    python3 ocr_4_forest_service/ocr_4_forest_service.py -i ocr_4_forest_service/inputs/forms/$input -json ocr_4_forest_service/inputs/jsons/template$number.json -temp ocr_4_forest_service/inputs/forms/template$number.jpg -p
else
    echo "---- You chose to run the Google Vision API."
    python3 ocr_4_forest_service/ocr_4_forest_service.py -i ocr_4_forest_service/inputs/forms/$input -json ocr_4_forest_service/inputs/jsons/template$number.json -temp ocr_4_forest_service/inputs/forms/template$number.jpg
fi



if [ $? -eq 0 ] 
then 
  printf "Code executed successfully.\n" 
else 
  printf "Code exited with error.\n"
fi

deactivate