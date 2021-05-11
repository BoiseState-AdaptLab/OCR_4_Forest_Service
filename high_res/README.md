## Experiment 2

In this second directory, I am working only with the high resolution form. We are currently extracting
the best single characters in the form by recording the xy-coordinates in a JSON file.

Step 1)
 * run **python crop_form.py** to extract the characters from the form;

Step 2) 
 * run **python img-preprocessing.py** to perform image preprocessing on each character;

Step 3)
 * run **python create_test_data.py** to create the csv file that will be the input for the OCR model;

##### Notes

The current preprocessing steps (GaussianBlur, THRESH_OTSU, GaussianBlur, cvtColor, Denoising) lead to
an accuracy score above 85%.  

The script named **gray.py** is used to make manual changes to the preprocessing of a single image, if necessary. 
 
