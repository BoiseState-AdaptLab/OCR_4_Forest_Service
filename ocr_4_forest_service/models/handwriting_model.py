# This file cotains the code that executes the model
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras import utils
import tensorflow.keras as keras
import json

HEIGHT = 28
WIDTH = 28
class_mapping = []
pred_data = {}


def main():

    # The location of the Kaggle EMNIST dataset
    TRAIN = "archive/" 
    train = pd.read_csv(os.path.join(TRAIN, 'emnist-balanced-train.csv'), header=None)

    # The location of the test dataset
    TEST = "../" 
    test = pd.read_csv(os.path.join(TEST, 'test_data.csv'), header=None)

    # setting up the field names to match with predictions for output
    field_name = test.loc[:, 785]
    test = test.iloc[: , :-1]

    field_name = field_name.to_numpy()

    for name in field_name:
        pred_data[name] = {'guesses' : [], 'pred_list': []}
    # print(pred_data)

    # The location to my Kaggle EMNIST mapping dataset
    mapp = pd.read_csv("archive/emnist-balanced-mapping.txt"
                       , delimiter = ' ', header=None, usecols=[1], squeeze=True)


    class_num = create_mapping(mapp)
   
    train_x, test_x = build_dataset(train, test)

    # create the "answer" key datasets
    train_y, test_y = create_answer(train, test)
 
    train_y, test_y = one_hot_encoding(train_y, test_y, class_num)
 
    train_x, test_x = data_reshape(train_x, test_x)
    
    model_1, model_2, model_3, model_4, model_5 = load_models()
    
    prediction_1, prediction_2, prediction_3, prediction_4, prediction_5 = predict_models(model_1, 
                                                                                            model_2, 
                                                                                            model_3, 
                                                                                            model_4, 
                                                                                            model_5, 
                                                                                            test_x)
    
    class_predictions_2 = predict_classes(model_1, 
                                            model_2, 
                                            model_3, 
                                            model_4, 
                                            model_5, 
                                            test_x)

    matchings = np.c_[class_predictions_2, field_name]
    # print(matchings)

    single_models(prediction_1, prediction_2, prediction_3, prediction_4, prediction_5, test_y, mapp, matchings) 
    
    # combine_models(prediction_1, prediction_2, prediction_3, prediction_4, prediction_5, 
    #                 test_y, pred_data, field_name, mapp)
    # print("we never return from here")

    return 0

def single_models(prediction_1, prediction_2, prediction_3, prediction_4, prediction_5, test_y, mapp, matchings):
    # pos_1 = all_guesses(prediction_1, test_y)
    # model_1_correct = correct_percentage_on_test(prediction_1, pos_1, test_y, mapp)
    pos_2 = all_guesses(prediction_2, test_y)
    model_2_correct = correct_percentage_on_test(prediction_2, pos_2, test_y, mapp, matchings)
    # pos_3 = all_guesses(prediction_1, test_y)
    # model_3_correct = correct_percentage_on_test(prediction_3, pos_3, test_y, mapp)
    # pos_4 = all_guesses(prediction_1, test_y)
    # model_4_correct = correct_percentage_on_test(prediction_4, pos_4, test_y, mapp)
    # pos_5 = all_guesses(prediction_1, test_y)
    # model_5_correct = correct_percentage_on_test(prediction_5, pos_5, test_y, mapp)

    print("\n")
    print('Accuracy of all 5 models used inside web application\n')
    # print('Model #1: {}%'.format(model_1_correct))
    print('Model #2: {}%'.format(model_2_correct))
    # print('Model #3: {}%'.format(model_3_correct))
    # print('Model #4: {}%'.format(model_4_correct))
    # print('Model #5: {}%'.format(model_5_correct))



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
        print(type(combined_model_prediction))
        # print(len(combined_model_prediction))

        print(type(field_name))
        print(len(field_name))

        # matchings = np.c_[combined_model_prediction.item(), field_name]
        matchings = np.column_stack((combined_model_prediction,field_name))
        values, pos = top_3(combined_model_prediction)

        for pred in pos[i]:
            preds.append(chr(mapp[pred]))


        if combined_model_prediction == np.argmax(test_y[i]):
            combined_correct += 1
            
        else:
            combined_incorrect += 1

        pred_data[matchings[i][1]]['guesses'].append(chr(mapp[np.argmax(combined_model_prediction[i])]))
        pred_data[matchings[i][1]]['pred_list'].append(preds)

    create_json(pred_data)

    accuracy_of_combined_models = (combined_correct / (combined_correct + combined_incorrect))* 100
    print('Accuracy of combined models: {}%'.format(accuracy_of_combined_models))



def create_json(pred_data):
    with open("field_preds.json", "w") as outfile:
        json.dump(pred_data, outfile)

def predict_classes(model_1, model_2, model_3, model_4, model_5, test_x):
    return model_2.predict_classes(test_x)


def predict_models(model_1, model_2, model_3, model_4, model_5, test_x):
    prediction_1 = model_1.predict(test_x)
    prediction_2 = model_2.predict(test_x)
    prediction_3 = model_3.predict(test_x)
    prediction_4 = model_4.predict(test_x)
    prediction_5 = model_5.predict(test_x)

    return prediction_1, prediction_2, prediction_3, prediction_4, prediction_5


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



def load_models():
    model_1 = keras.models.load_model("models/model_1.h5") # 2-conv-128-nodes-2-dense-0.2-Dropout
    model_2 = keras.models.load_model("models/model_2.h5") # 2-conv-128-nodes-2-dense-0.2-Dropout
    model_3 = keras.models.load_model("models/model_3.h5") # 2-conv-64-nodes-2-dense-0.2-Dropout
    model_4 = keras.models.load_model("models/model_4.h5") # 2-conv-64-nodes-2-dense-0.2-Dropout
    model_5 = keras.models.load_model("models/model_5.h5")# 2-conv-64-nodes-2-dense-0.2-Dropout

    return model_1, model_2, model_3, model_4, model_5



def data_reshape(train_x, test_x):
    # reshape the data to have 4 dimentions
    train_x = train_x.reshape(-1, HEIGHT, WIDTH, 1)
    test_x = test_x.reshape(-1, HEIGHT, WIDTH, 1)

    return train_x, test_x



def create_answer(train, test):
    train_y = train.iloc[:,0]
    test_y = test.iloc[:,0]

    return train_y, test_y



def one_hot_encoding(train_y, test_y, class_num):
    # perform One Hot Encoding to get the data ready for model
    train_y = utils.to_categorical(train_y, class_num)
    test_y = utils.to_categorical(test_y, class_num)

    return train_y, test_y



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
            # print("\n")
            # print(f"{x})")
            # print("guess: ", np.argmax(predictions[x]), "--> ", chr(mapp[np.argmax(predictions[x])]))
            # print("class: ", np.argmax(test_y[x]),  "--> ", chr(mapp[np.argmax(test_y[x])]))
            correct += 1
            # print("## correct")
        else:
            # print("\n")
            # print(f"{x})")
            # print("guess: ", np.argmax(predictions[x]), "--> ", chr(mapp[np.argmax(predictions[x])]))
            # print("class: ", np.argmax(test_y[x]),  "--> ", chr(mapp[np.argmax(test_y[x])]))

            # print(preds)

            incorrect += 1
            # print("incorrect")

        pred_data[matchings[x][1]]['guesses'].append(chr(mapp[np.argmax(predictions[x])]))
        pred_data[matchings[x][1]]['pred_list'].append(preds)
    
    create_json(pred_data)

    return (correct / (correct + incorrect)) * 100



def build_dataset(train, test):
    train_x = []
    test_x = []

    for i in range(len(train)):
        train_x.append(convert_training_data(train,i))

    for i in range(len(test)):
        test_x.append(convert_training_data(test,i))

    train_x = np.asarray(train_x)
    test_x = np.asarray(test_x)


    # normalize the data
    train_x = train_x.astype('float32')
    train_x /= 255
    test_x = test_x.astype('float32')
    test_x /= 255

    return train_x, test_x



def convert_training_data(df,row):
    pxl_data = df.values[row,1:]
    # Reshape the image coming in
    pxl_reshape = pxl_data.reshape(HEIGHT,WIDTH)
    # Invert the image
    final_img = np.transpose(pxl_reshape, axes=[1,0])
    return final_img



def get_char(df, row):
    return class_mapping[df.values[row,0]]



if __name__ == '__main__':
  main()
