import io
import os
import json
import cv2
from google.cloud import vision_v1p3beta1 as vision


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/florianaciaglia/Desktop/forestservice-331216-d7b2871c2dfe.json' # this needs to be changed to Cathie's account

TOP_FORM = ['WRITEUP NO.', 'PHOTO NO.', 'FOREST', 'RANGER DISTRICT', 'ALLOTMENT', 'EXAMINER', 'DATE', 
            'TRANSECT NO.', 'PLOT SIZE', 'PLOT INTERVAL', 'TYPE DESIGNATION', 'KINF OF LIVESTOCK', 'SLOPE',
            'EXPOSURE', 'ASPECT', 'LOCATION', 'ELEVATION']

def google_vision_char_detection(field_images):
    pred_json = {}
   
    for image, field_name in field_images:
     
        # for now, we are just working on the
        # top fields of the form
        if field_name in TOP_FORM:
         
            # this dictionary keeps track of
            # the OCR results
            pred_json[field_name] = {}
          
            detect_handwritten_ocr(image, pred_json[field_name])
    
    # Store all our results into JSON file
    with open('google_vision_results.json', 'w') as outfile:
        json.dump(pred_json, outfile)


def detect_handwritten_ocr(image, json_list):
    """Detects handwritten characters in a local image.

    Args:
    image: numpy array of our field image
    """
    
    client = vision.ImageAnnotatorClient()

    # read numpy array as a byte string and directly pass it to Vision API
    image = vision.Image(content=cv2.imencode('.jpg', image)[1].tostring())
  
    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image,
                                              image_context=image_context)


    json_list['Full text'] = response.full_text_annotation.text.replace("\n", " ")

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
        
            json_list['Block confidence'] = block.confidence
            for paragraph in block.paragraphs:
            
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
        


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

