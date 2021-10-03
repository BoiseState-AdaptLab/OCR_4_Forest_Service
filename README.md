# OCR_4_Forest_Service

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [UML Diagram](#uml-diagram)


## General info
OCR_4_Forest_Service implements a pdf processing pipeline used to extract handwritten words from the Forest Serive forms. 
	
## Technologies
Project is created with:
* Python: 3.7
* OpenCV: 4.5
	
## Setup
To run this project, clone it locally using the following command:

```
$ git clone https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service.git
```
Once cloned, navigate to the `ocr_4_forest_service` directory:
```
$ cd OCR_4_Forest_Service/ocr_4_forest_service/
```
The pipeline can be run in **production** mode or **testing** mode (`-t`).
- The production mode will perfom character detection on the provided pdf form. Therefore, the OCR will not be provided with labels for classification. The label for each image is set to a fictitious value.
- The testing model will not perform character detection. The labels are set to true values we manually generated for testing purposes. By running this version of the pipeline, we are able to evaluate the accuracy of the entire pipeline. 

### Parameters

- `-i`: input file. The pdf form provided by the Forest Service. The Forest Service has three different versions of this file. 
- `-json`: JSON file with the fields' coordinates. Since each of the three input file versions have different field layouts, we created three JSON files with the correct coordinates to locate the fields. Depending on the form version you are using, there will be a json file with the correct coordinates inside the `inputs/jsons/` directory: `template1_field_coord.json`, `template2_field_coord.json`, and `template3_field_coord.json`.
	**Keep reading to find out what template to use.**
- `-temp`: template to allign the form. Form allignment is fundamental for correct character detection in the form. Inside the `inputs/forms/` directory, you will find three files, among others, named `template1.jpg`, `template2.jpg`, and `template3.jpg`. 

	* We mapped Site Analysis Summary forms with the *% Dry Wt* field on the right side of the form as `template1.jpg`:
	 <img src="https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/ocr_4_forest_service/inputs/forms/template1.jpg" alt="template 1" width="400"/>
	
	* We mapped Site Analysis Summary forms with the *% Dry Wt* field right next to the *Species* field as `template2.jpg`:
	 <img src="https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/ocr_4_forest_service/inputs/forms/template2.jpg" alt="template 2" width="400"/>
	
	 
	* We mapped the Site Analysis forms as `template3.jpg`
	 <img src="https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/ocr_4_forest_service/inputs/forms/template3.jpg" alt="template 3" width="400"/>
	
	 
## Run Pipeline

To run the production pipeline:
```
$ python ocr_4_forest_service -i <name-of-pdf-form> -json <json-coordinate-file> -temp <template-for-file-alignment>
```

Thid command will create a csv file called `test_data.csv` that will be the input to the Optical Character Recognition model. 

If you want to run the testing pipeline, run the following code (The same as above but followed by the `-t` flag):
```
$ python ocr_4_forest_service -i <name-of-pdf-form> -json <json-coordinate-file> -temp <template-for-file-alignment> -t
```
`Note`: When running the testing pipeline, the json file needs to include labels for each field. We provide some instances of these files inside the `inputs/jsons
` directory, each named after the input form.  


## UML Diagram
![alt text](https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/visuals/data-pipeline-production.jpg)
