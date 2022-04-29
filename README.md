# OCR_4_Forest_Service

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Pre-Setup](#pre-setup)
* [Setup](#setup)


## General info
OCR_4_Forest_Service implements a pdf processing pipeline used to extract handwritten words from the Forest Service forms. All the code can be executed using the bash scripts under the ```exec/``` folder and detected data is stored into the Forest Service database using files in the ```db/``` folder. 
	
## Technologies
Make sure you have the following installed:
* Python: 3.7
* Git

## Pre-Setup

The structure of this repository assumes that you have installed postgres from source under a folder called ```tools``` on the same level as this repo's. We are also assuming that the database folder is at that same root level and is called ```forest_data```.
	
## Setup
To run this project, clone it locally using the following command:

```
$ git clone https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service.git
```
Once cloned, navigate to the `ocr_4_forest_service` directory:
```
$ cd OCR_4_Forest_Service/
```
The pipeline can be run in **production** mode or **testing** mode (`-t`).
- The production mode will perfom character detection on the provided pdf form. Therefore, the OCR will not be provided with labels for classification. The label for each image is set to a fictitious value.
- The testing model will not perform character detection. The labels are set to true values we manually generated for testing purposes. By running this version of the pipeline, we are able to evaluate the accuracy of the entire pipeline. :no_entry_sign:```NOTE: with the automation currently in place the testing mode might not work. This feature might need further work.```

After having clones the repo and having cd'ed into it, the program can be run using the following command:

-- Run everything under ```OCR_4_Forest_Service/```

1) ```bash exec/step0_initialize_db.sh``` This file needs to be executed only one. WARNING:warning:: if you run this file more than once, the data stored in the database up to that point will be lost. 
2) The execution of ```step1_connect_db.sh``` can be skipped if no database issues have occurred. 
3) ```bash exec/step2_generate_data.sh -i <input file name> -v <pipeline/google> -n <1/2/3>``` This script creates the virtual enviroment and installs the packages needed to run the pipeline. The first time you run this file, execution will take longer because all packages needs to be installed. This script also runs the entire pipeline and stores the results into the database. We need to provide the name of the input file, the version of the program that we want to run (either our pipeline or the google vision API). :no_entry_sign:```NOTE: if you want to run the google vision API you need to navigate to the db/orm_scripts/create_report.py file and change the name of the json file you want to read from on line 15. Follow in-file comments to make this change.```  Example of command ```bash exec/step2_generate_data.sh -i test9.jpeg -v pipeline -n 3```
5) Run ```bash exec/step3_save_leave.sh``` when you are done processing files and you want to disconnect from the database server. 

### Pipeline's Parameters

You don't have to worry about the direct parameters for the pipeline because the bash scripts above take care of those for you. But if you are curious, this is how it's set up:

- `-i`: input file. The pdf form provided by the Forest Service. The Forest Service has three different versions of this file. 
- `-json`: JSON file with the fields' coordinates. Since each of the three input file versions have different field layouts, we created three JSON files with the correct coordinates to locate the fields. Depending on the form version you are using, there will be a json file with the correct coordinates inside the `inputs/jsons/` directory: `template1_field_coord.json`, `template2_field_coord.json`, and `template3_field_coord.json`.
	**Keep reading to find out what template to use.**
- `-temp`: template to allign the form. Form allignment is fundamental for correct character detection in the form. Inside the `inputs/forms/` directory, you will find three files, among others, named `template1.jpg`, `template2.jpg`, and `template3.jpg`. 

### Template numbers

When runninig the second bash script (```bash exec/step2_generate_data.sh```), you'll need to know what version of template you are running. Follow the images below as a reference. 

* We mapped Site Analysis Summary forms with the *% Dry Wt* field on the right side of the form as `template1.jpg`:
<img src="https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/ocr_4_forest_service/inputs/forms/template1.jpg" alt="template 1" width="400"/>
	
* We mapped Site Analysis Summary forms with the *% Dry Wt* field right next to the *Species* field as `template2.jpg`:
<img src="https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/ocr_4_forest_service/inputs/forms/template2.jpg" alt="template 2" width="400"/>
	
	 
* We mapped the Site Analysis forms as `template3.jpg`
<img src="https://github.com/BoiseState-AdaptLab/OCR_4_Forest_Service/blob/main/ocr_4_forest_service/inputs/forms/template3.jpg" alt="template 3" width="400"/>
	
	 
## Run Pipeline (The user doesn't need to worry about this section)

To run the production pipeline:
```
$ python ocr_4_forest_service.py -i <name-of-pdf-form> -json <json-coordinate-file> -temp <template-for-file-alignment>
```

Thid command will create a csv file called `test_data.csv` that will be the input to the Optical Character Recognition model. 

If you want to run the testing pipeline, execute the following command (The same as above but followed by the `-t` flag):
```
$ python ocr_4_forest_service.py -i <name-of-pdf-form> -json <json-coordinate-file> -temp <template-for-file-alignment> -t
```
`Note`: When running the testing pipeline, the json file needs to include labels for each field. We provide some instances of these files inside the `inputs/jsons` directory, each named after the input form.  


## Known Issues that need to be fixed -- Future Work
There's some known bugs that this software has that need to be fixed. This is not a comprehensive list of bugs but it's rather a place to start. 

* Under ```ocr_4_forest_service/model/handwriting_model.py``` several statements have deprecation warnings that need to be fixed. 
* Implement a way to detemine if we want to read from ```google_vision_results.json``` or ```field_preds.json``` in ```db/orm_scripts/create_report.py```
* At the moment, if the pipeline doesn't find any data in a field the data point gets automatically set to 'null'. We might want to find a better solution for this case. 
* Depending on the file that is being used as input, the fields might have an EXPOSURE or an ASPECR title. The ```db/orm_scripts/create_report.py``` file needs to be updated on line 114 to call the correct function between get_exposure() or get_aspect(). This issue needs a better solution. 
