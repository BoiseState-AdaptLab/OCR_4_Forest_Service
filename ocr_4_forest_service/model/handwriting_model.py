# This file cotains the code that executes the model
import numpy as np
import os
import pandas as pd
from tensorflow.keras import utils
import tensorflow.keras as keras
import argparse
import json

HEIGHT = 28
WIDTH = 28
class_mapping = []
pred_data = {}

#used to be main
def run_model():

    input = "test_data.csv"
    # ../../OCR_4_Forest_Service/ocr_4_forest_service/
    # ../../OCR_4_Forest_Service/ocr_4_forest_service/
    mapping = "ocr_4_forest_service/model/datasets/emnist-balanced-mapping.txt"
    model = "ocr_4_forest_service/model/models/model_2.h5"


    # load the csv file as test data 
    test = pd.read_csv(input, header=None)

    # setting up the field names to match with predictions for output
    field_name = test.loc[:, 785]
    test = test.iloc[: , :-1]

    # turn field names to numpy arrays
    field_name = field_name.to_numpy()

    # set up the format of the output json file
    for name in field_name:
        pred_data[name] = {'Full text' : [], 'pred_list': []}


    # load Kaggle EMNIST mapping dataset
    mapp = pd.read_csv(mapping, delimiter = ' ', header=None, usecols=[1], squeeze=True)

    # mapps each letter to a number
    class_num = create_mapping(mapp)
   
    test_x = build_dataset(test)

    # create the "answer" key datasets
    test_y = create_answer(test)
 
    test_y = one_hot_encoding(test_y, class_num)
 
    test_x = data_reshape(test_x)
    
    # load the pre-trained model_2
    model = load_model(model)

    # call predict on the classes labels
    predictions = predict_classes(test_x, model)
    
    
    # get model predictions on each image in test
    final_model_prediction = predict_models(model, test_x)
   

    # matches each image to its field name 
    matchings = np.c_[predictions, field_name]


    # runs the model classification and stores data into pred_data
    accuracy_score = single_models(final_model_prediction, test_y, mapp, matchings) 


    with open("field_preds.json", "w") as outfile:  
        json.dump(pred_data, outfile)

    return 0


def predict_classes(test_x, model):
    return model.predict_classes(test_x) 


def single_models(final_model_prediction, test_y,mapp, matchings):
    
    values, pos = top_3(final_model_prediction, test_y)
    return correct_percentage_on_test(final_model_prediction, pos, test_y, mapp, matchings)
    


def combine_models(prediction_1, prediction_2, prediction_3, prediction_4, prediction_5, test_y, pred_data,  field_name, mapp):
    combined_correct = 0
    combined_incorrect = 0

    for i in range(len(test_y)):

        preds = []
        

        model_1_pred = np.argmax(prediction_1[i])
        model_2_pred = np.argmax(prediction_2[i])
        model_3_pred = np.argmax(prediction_3[i])
        model_4_pred = np.argmax(prediction_4[i])
        model_5_pred = np.argmax(prediction_5[i])


        combined_model_prediction = model_jury_ruling(model_1_pred, model_2_pred, model_3_pred, model_4_pred, model_5_pred)
        # print(type(combined_model_prediction))
        # print(len(combined_model_prediction))

        # print(type(field_name))
        # print(len(field_name))

        # matchings = np.c_[combined_model_prediction.item(), field_name]
        matchings = np.column_stack((combined_model_prediction,field_name))
        values, pos = top_3(combined_model_prediction)

        for pred in pos[i]:
            preds.append(chr(mapp[pred]))


        if combined_model_prediction == np.argmax(test_y[i]):
            combined_correct += 1
            
        else:
            combined_incorrect += 1

        pred_data[matchings[i][1]]['Full text'].append(chr(mapp[np.argmax(combined_model_prediction[i])]))
        pred_data[matchings[i][1]]['pred_list'].append(preds)

    create_json(pred_data)

    accuracy_of_combined_models = (combined_correct / (combined_correct + combined_incorrect))* 100
    # print('Accuracy of combined models: {}%'.format(accuracy_of_combined_models))



def create_json(pred_data):
    with open("field_preds.json", "w") as outfile:
        json.dump(pred_data, outfile)




def predict_models(model_2, test_x):
   
    prediction_2 = model_2.predict(test_x)
  
    return prediction_2


def top_3(predictions, test_y):
    all_values = []
    all_pos = []
    
    for x in range(len(test_y)):
        ranks = sorted( [(x,i) for (i,x) in enumerate(predictions[x])], reverse=True )
        values = []
        posns = []
        for x,i in ranks:
            if x not in values:
                values.append( x )
                posns.append( i )
                if len(values) == 47:
                    break
        all_values.append(values)
        all_pos.append(posns)
    return all_values, all_pos



def load_model(model):
    
    model_2 = keras.models.load_model(model) # 2-conv-128-nodes-2-dense-0.2-Dropout
    
    return model_2



def data_reshape(test_x):
    # reshape the data to have 4 dimentions
    test_x = test_x.reshape(-1, HEIGHT, WIDTH, 1)

    return test_x



def create_answer(test):
    test_y = test.iloc[:,0]

    return test_y



def one_hot_encoding(test_y, class_num):
    # perform One Hot Encoding to get the data ready for model
    test_y = utils.to_categorical(test_y, class_num)

    return test_y



def create_mapping(mapp):
    for num in range(len(mapp)):
        class_mapping.append(chr(mapp[num]))

    class_num = len(class_mapping)

    return class_num



def make_prediction(model, img):
    prediction = model.predict(img)
    idx_prediction = np.argmax(prediction[0])
    return class_mapping[idx_prediction]



def model_jury_ruling(*argv):
    all_predictions = []
    for arg in argv:
        all_predictions.append(arg)

    hash = {}

    for prediction in all_predictions:
        if prediction not in hash:
            hash[prediction] = 1
        else:
            hash[prediction] += 1

    # If all models do not have a unanimous vote, majority rules
    # Note: If there is a tie, the first item of the tie that is added gets priority over rest of the items
    return max(hash, key=hash.get)



def all_guesses(predictions, test_y):
    all_values = []
    all_pos = []
    
    for x in range(len(test_y)):
        ranks = sorted( [(x,i) for (i,x) in enumerate(predictions[x])], reverse=True )
        values = []
        posns = []
        for x,i in ranks:
            if x not in values:
                values.append( x )
                posns.append( i )
                if len(values) == 47:
                    break
        all_values.append(values)
        all_pos.append(posns)
    return all_pos



def correct_percentage_on_test(predictions, pos, test_y, mapp, matchings):
        
    correct = 0
    incorrect = 0

    for x in range(len(test_y)):
        preds = []
        for pred in pos[x]:
            preds.append(chr(mapp[pred]))
         

        if np.argmax(predictions[x]) == np.argmax(test_y[x]):
            
            correct += 1
            # print("## correct")
        else:
            
            incorrect += 1
            # print("incorrect")

        # print("this is pred data", pred_data)
        # print(" ")

        # print("this is matchings", matchings)
        # print("*** here", pred_data[matchings[x][1]]['Full text'])


      
        pred_data[matchings[x][1]]['Full text'].append(chr(mapp[np.argmax(predictions[x])]))
        pred_data[matchings[x][1]]['pred_list'].append(preds)
    
    create_json(pred_data)

    return (correct / (correct + incorrect)) * 100



def build_dataset(test):
    
    test_x = []

    for i in range(len(test)):
        test_x.append(convert_training_data(test,i))

    test_x = np.asarray(test_x)

    # normalize the data
    test_x = test_x.astype('float32')
    test_x /= 255

    return test_x



def convert_training_data(df,row):
    pxl_data = df.values[row,1:]
    # Reshape the image coming in
    pxl_reshape = pxl_data.reshape(HEIGHT,WIDTH)
    # Invert the image
    final_img = np.transpose(pxl_reshape, axes=[1,0])
    return final_img



def get_char(df, row):
    return class_mapping[df.values[row,0]]



# if __name__ == '__main__':
#   main()
