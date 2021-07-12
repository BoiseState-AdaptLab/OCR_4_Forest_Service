## Experiment 1

In this directory, we are working on the first form sample we received - template.pdf. This form has
better handwriting samples but lower image resolution. We have extracted about 100 samples of characters. 

The input images are stored in the images/ directory. 

The following are the steps to set up the data:
 
Step 1)
* run **python crop_form.py** to extract the characters from the form;

Step 2)
* run **python img-preprocessing.py** to perform image preprocessing on each character;

Step 3)
* run **python create_test_data.py** to create the csv file that will be the input for the OCR model;

##### Notes
The accuracy score has never passed 50% becuse of the lower image resolution and noise aroud the letters. 

