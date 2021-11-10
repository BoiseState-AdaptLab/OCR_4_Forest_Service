import io
import os
import json
import cv2
from google.cloud import vision_v1p3beta1 as vision


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/florianaciaglia/Desktop/forestservice-331216-d7b2871c2dfe.json'

TOP_FORM = ['WRITEUP NO.', 'PHOTO NO.', 'FOREST', 'RANGER DISTRICT', 'ALLOTMENT', 'EXAMINER', 'DATE', 
            'TRANSECT NO.', 'PLOT SIZE', 'PLOT INTERVAL', 'TYPE DESIGNATION', 'KINF OF LIVESTOCK', 'SLOPE',
            'EXPOSURE', 'ASPECT', 'LOCATION', 'ELEVATION']

def google_vision_char_detection(field_images):
    pred_json = {}
   
    for image, field_name in field_images:
     
        if field_name in TOP_FORM:
         
            pred_json[field_name] = {}
          
            detect_handwritten_ocr(image, pred_json[field_name])
    
    with open('google_vision_results.json', 'w') as outfile:
        json.dump(pred_json, outfile)


def detect_handwritten_ocr(image, json_list):
    """Detects handwritten characters in a local image.

    Args:
    path: The path to the local file.
    """
    
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=cv2.imencode('.jpg', image)[1].tostring())
  
    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image,
                                              image_context=image_context)


    # print('Full Text: {}'.format(response.full_text_annotation.text))
    
    json_list['Full text'] = response.full_text_annotation.text.replace("\n", " ")

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print('\nBlock confidence: {}\n'.format(block.confidence))
            json_list['Block confidence'] = block.confidence
            for paragraph in block.paragraphs:
                # print('Paragraph confidence: {}'.format(
                #     paragraph.confidence))
                # json_list['Paragraph confidence'] = paragraph.confidence
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    # print('Word text: {} (confidence: {})'.format(
                    #     word_text, word.confidence))
                    # json_list['Word text'] = word_text
                    # json_list['Word text - confidence'] = word.confidence
                    # for symbol in word.symbols:
                        # print('\tSymbol: {} (confidence: {})'.format(
                        #     symbol.text, symbol.confidence))
                        # json_list['Symbol'] = symbol.text
                        # json_list['Symbol - confidence'] = symbol.confidence


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

# if __name__ == '__main__':
#   main()