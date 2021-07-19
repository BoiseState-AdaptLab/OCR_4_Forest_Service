# This file contains tests character detection functionalities on single fields

from ..src.char_detection import find_char
from ..src.char_detection import create_json
from ..src.char_detection import word_segmentation
from ..src.crop_bbox import output_dir
from ..src.crop_bbox import crop
import cv2
import os
import json
import shutil


def test_field_0():
    DIR = 'fields/'
    image = 'field_0.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_0_coord.json"):
        file = open("field_0_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_0_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_0'):
        try:
            shutil.rmtree('field_0')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_0'):
        os.makedirs('field_0')
    

    json_file = open('field_0_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_0/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_0/'):
        count = count + 1
   
    assert count == 3


def test_field_1():
    DIR = 'fields/'
    image = 'field_1.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_1_coord.json"):
        file = open("field_1_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_1_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_1'):
        try:
            shutil.rmtree('field_1')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_1'):
        os.makedirs('field_1')
    

    json_file = open('field_1_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_1/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_1/'):
        count = count + 1
   
    assert count == 8


def test_field_2():
    DIR = 'fields/'
    image = 'field_2.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_2_coord.json"):
        file = open("field_2_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_2_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_2'):
        try:
            shutil.rmtree('field_2')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_2'):
        os.makedirs('field_2')
    

    json_file = open('field_2_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_2/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_2/'):
        count = count + 1
   
    assert count == 8


def test_field_3():
    DIR = 'fields/'
    image = 'field_3.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_3_coord.json"):
        file = open("field_3_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_3_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_3'):
        try:
            shutil.rmtree('field_3')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_3'):
        os.makedirs('field_3')
    

    json_file = open('field_3_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_3/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_3/'):
        count = count + 1
   
    assert count == 10


def test_field_4():
    DIR = 'fields/'
    image = 'field_4.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_4_coord.json"):
        file = open("field_4_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_4_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_4'):
        try:
            shutil.rmtree('field_4')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_4'):
        os.makedirs('field_4')
    

    json_file = open('field_4_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_4/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_4/'):
        count = count + 1
   
    assert count == 10


def test_field_5():
    DIR = 'fields/'
    image = 'field_5.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_5_coord.json"):
        file = open("field_5_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_5_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_5'):
        try:
            shutil.rmtree('field_5')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_5'):
        os.makedirs('field_5')
    

    json_file = open('field_5_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_5/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_5/'):
        count = count + 1
   
    assert count == 9



def test_field_6():
    DIR = 'fields/'
    image = 'field_6.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_6_coord.json"):
        file = open("field_6_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_6_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_6'):
        try:
            shutil.rmtree('field_6')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_6'):
        os.makedirs('field_6')
    

    json_file = open('field_6_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_6/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_6/'):
        count = count + 1
   
    assert count == 6


def test_field_7():
    DIR = 'fields/'
    image = 'field_7.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_7_coord.json"):
        file = open("field_7_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_7_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_7'):
        try:
            shutil.rmtree('field_7')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_7'):
        os.makedirs('field_7')
    

    json_file = open('field_7_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_7/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_7/'):
        count = count + 1
   
    assert count == 3


def test_field_8():
    DIR = 'fields/'
    image = 'field_8.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_8_coord.json"):
        file = open("field_8_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_8_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_8'):
        try:
            shutil.rmtree('field_8')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_8'):
        os.makedirs('field_8')
    

    json_file = open('field_8_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_8/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_8/'):
        count = count + 1
   
    assert count == 3


def test_field_9():
    DIR = 'fields/'
    image = 'field_9.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_9_coord.json"):
        file = open("field_9_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_9_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_9'):
        try:
            shutil.rmtree('field_9')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_9'):
        os.makedirs('field_9')
    

    json_file = open('field_9_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_9/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_9/'):
        count = count + 1
   
    assert count == 3

def test_field_10():
    DIR = 'fields/'
    image = 'field_10.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_10_coord.json"):
        file = open("field_10_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_10_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_10'):
        try:
            shutil.rmtree('field_10')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_10'):
        os.makedirs('field_10')
    

    json_file = open('field_10_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_10/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_10/'):
        count = count + 1
   
    assert count == 7


def test_field_11():
    DIR = 'fields/'
    image = 'field_11.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_11_coord.json"):
        file = open("field_11_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_11_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_11'):
        try:
            shutil.rmtree('field_11')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_11'):
        os.makedirs('field_11')
    

    json_file = open('field_11_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_11/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_11/'):
        count = count + 1
   
    assert count == 5


def test_field_12():
    DIR = 'fields/'
    image = 'field_12.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_12_coord.json"):
        file = open("field_12_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_12_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_12'):
        try:
            shutil.rmtree('field_12')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_12'):
        os.makedirs('field_12')
    

    json_file = open('field_12_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_12/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_12/'):
        count = count + 1
   
    assert count == 2


def test_field_13():
    DIR = 'fields/'
    image = 'field_13.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_13_coord.json"):
        file = open("field_13_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_13_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_13'):
        try:
            shutil.rmtree('field_13')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_13'):
        os.makedirs('field_13')
    

    json_file = open('field_13_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_13/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_13/'):
        count = count + 1
   
    assert count == 4

def test_field_14():
    DIR = 'fields/'
    image = 'field_14.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_14_coord.json"):
        file = open("field_14_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_14_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_14'):
        try:
            shutil.rmtree('field_14')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_14'):
        os.makedirs('field_14')
    

    json_file = open('field_14_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_14/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_14/'):
        count = count + 1
   
    assert count == 30

def test_field_15():
    DIR = 'fields/'
    image = 'field_15.jpg'
	
    list_of_dict = []
    json_dict = {} 

    # if the output file has already been generated, 
    # clean it out before appending to it
    if os.path.exists("field_15_coord.json"):
        file = open("field_15_coord.json","r+")
        file.truncate(0)
        file.close()
    path = DIR + image
    img = cv2.imread(path, 0) 

    #perform the image preprocessing stepss
    #blurred = cv2.GaussianBlur(img, (3,3), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    con_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #dst = cv2.fastNlMeansDenoisingColored(con_img, None, 10, 10, 7, 21)
        
    json_data = find_char(con_img, image, json_dict)
    list_of_dict.append(json_data)

    create_json(list_of_dict)
  
    json_file = word_segmentation()
    # store the data into a new json file
    with open("field_15_coord.json", 'w') as outfile: 
        json.dump(json_file, outfile)

    # the last call to create_json() generates the 
    # json file with the coordinates of all the chars
    # detected in field_0.jpg
    # if it already exists, clean it
    if os.path.exists('field_15'):
        try:
            shutil.rmtree('field_15')
        except:
            print("Error: couldn't clean the single_chars/ directory")
    # else, create it
    if not os.path.exists('field_15'):
        os.makedirs('field_15')
    

    json_file = open('field_15_coord.json')
    fields = json.load(json_file)
    i = 0
    for dict in fields:
         # we only get the key
        new_d = [str(key) for key in dict.keys()]
       
        field_name = DIR + new_d[0]

        # open form as an image
        img = cv2.imread(field_name)

        for boxes in dict.values():
            for box in boxes:

                x = box['x']
                y = box['y']
                w = box['w']
                h = box['h']

                # cropping the image
                cropped_img = img[y:y + h, x:x + w]

                # display the image to user
                if cropped_img is not None:
                    
                    cv2.imwrite('field_15/box_{num}.jpg'.format(num = i), cropped_img)

                else:
                    print("no image has been read")

                i = i + 1 

    # now, we need to assest that the amount of images 
    # stored in the single_chars/ is equal to the amount
    # of letters contained in field_0.jpg

    count = 0
    for img in os.listdir('field_15/'):
        count = count + 1
   
    assert count == 4
