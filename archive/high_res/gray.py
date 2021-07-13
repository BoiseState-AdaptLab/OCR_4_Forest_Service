import cv2
import numpy as np
from matplotlib import pyplot as plt

cv_img = cv2.imread("output/field_4.jpg", 0)
#green_channel = cv_img[:,:,1]
#red_channel = cv_img[:,:,0]
#blue_channel = cv_img[:,:,2]
#print(cv_img.shape)
blurred = cv2.GaussianBlur(cv_img, (3,3), cv2.BORDER_DEFAULT)
hist = plt.hist(blurred.ravel(),256,[0,256]);
plt.show()
# 25% of 28x28 pixels (784) is 196 pixels.
# iterate, starting from the right side, through
# the first 196 pixels and add up their x values.
x_value = {}
counter = 0
add = 0
for item in hist[0]:
  x_value[counter] = item
  counter = counter + 1

x_list = list(x_value.values())
for i in x_list:
  if add < 196:
    add = add + i
  else:
    print(i)
    break

for i, x in x_value.items():
  if x == 10:
    print("interested: ",i)

## I GOT 163 AS THE NUMBER FOR THE DARKEST 25%
## HAVING 157 AS THE NUMBER FOR THRESH IS BETTER

 
#plt.show()
#plt.hist(red_channel.ravel(),256,[0,256]);
#plt.show()
#plt.hist(blue_channel.ravel(),256,[0,256]);
# create empty image with same shape as that of src image
#green_img = np.zeros(cv_img.shape)
#assign the green channel of src to empty image
#green_img[:,:,1] = green_channel

# create empty image with same shape as that of src image
#red_img = np.zeros(cv_img.shape)
#assign the green channel of src to empty image
#red_img[:,:,0] = red_channel
#cv2.imwrite("red.png", red_channel)
# create empty image with same shape as that of src image
#blue_img = np.zeros(cv_img.shape)
#assign the green channel of src to empty image
#blue_img[:,:,2] = blue_channel
#save image
#cv2.imwrite('cv2-green-channel.png',green_img)

#print("we passed it")
#plt.show()
#exit(0)
if cv_img is None:
  print("error")
#show the histogram
#hist = plt.hist(cv_img.ravel(), 256, [0,256]);
#plt.show()

#cv2.imshow("original", cv_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#cv2.imshow("green", green_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imshow("red", red_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imshow("blue", blue_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#hist = cv2.calcHist([cv_img], [0], None, [256], [0,255])

#if hist is None:
#  print("error here")
#plt.subplot(),plt.imshow(hist),plt.title('hist')
#plt.xticks([]), plt.yticks([])
#plt.show()

ret, thresh = cv2.threshold(cv_img, 155, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("thresholded", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("thresh.png", thresh)

blurred = cv2.GaussianBlur(thresh, (3,3), cv2.BORDER_DEFAULT)
cv2.imshow("Blurred", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("blurred.png", blurred)
con_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
dst = cv2.fastNlMeansDenoisingColored(con_img,None,10,10,7,21)
cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("dst.png", dst)
