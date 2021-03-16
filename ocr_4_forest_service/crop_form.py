#Author: Floriana Ciaglia
# Data: March 8, 2021
# https://yangcha.github.io/iview/iview.html
import cv2
import os
import string
import json

def main():
    path = None
    window_name = "image"
    i = 0
    #prompt user for input
    if(path is not 'q'):
        path  = input("Enter the path to the Forest Service Sheet or type q to quit: ")
        

        while not os.path.isfile(path):
            
            if path == 'q':
                exit(0)
            path = input("** The file could not be found ** \n Enter a valid path to the file: ")
            
        
        #open file as an image
        img = cv2.imread(path)
        
        #load the json file
        jsonFile = open('data/fields.json')
        fields = json.load(jsonFile)
    
        #
        for field in fields:
           #print(field)
            x = int(field["x"])
            y = int(field["y"])
            w = int(field["width"])
            h = int(field["height"])


            #cropping the image
            cropped_img = crop(img, x, y, w, h)
            

            #display the image to user
            if cropped_img is not None:
                cv2.imshow(window_name, cropped_img)
                cv2.imwrite('field_{:>02}.jpg'.format(i), cropped_img)
            else:
                print("no image has been read")
            
            i += 1
            cv2.waitKey(0)  
            cv2.destroyAllWindows()
            cv2.destroyWindow(window_name)
            cv2.waitKey(10)  

        jsonFile.close()
    exit(0)

#cropping function
def crop(image, x, y, w, h):
    cropped = image[y:y+h, x:x+w]
    
    return cropped

#function to resize found on https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv

#main function 
if __name__ == '__main__':
    main()
