#!/usr/bin/env python
# Author: Sandra Busch
# Date: June 14, 2021
import os
import cv2
import numpy as np
import imutils

def main():
    imagePath = None
    templatePath = None
    maxFeatures = 1000
    keepPercent = 0.2

    # prompt user for input
    if (templatePath != 'q' or imagePath != 'q'):
        templatePath = input("Enter the path to the template or type q to quit: ")
        while not os.path.isfile(templatePath):
            if templatePath == 'q':
                exit(0)
            templatePath = input("** The file could not be found ** \n Enter a valid path to the file: ")
        imagePath = input("Enter the path to image being aligned or type q to quit: ")
        while not os.path.isfile(imagePath):
            if imagePath == 'q':
                exit(0)
            imagePath = input("** The file could not be found ** \n Enter a valid path to the file: ")

        # open file as an image
        image = cv2.imread(imagePath)
        template = cv2.imread(templatePath)

        # convert both the input image and template to grayscale
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # use ORB to detect keypoints and extract (binary) local
        # invariant features
        orb = cv2.ORB_create(maxFeatures)
        (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
        (kpsB, descsB) = orb.detectAndCompute(templateGray, None)

        # match the features
        method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
        matcher = cv2.DescriptorMatcher_create(method)
        matches = matcher.match(descsA, descsB, None)

        # sort the matches by their distance (the smaller the distance,
        # the "more similar" the features are)
        matches = sorted(matches, key=lambda x: x.distance)

        # keep only the top matches
        keep = int(len(matches) * keepPercent)
        matches = matches[:keep]

        # check to see if we should visualize the matched keypoints
        # if debug:
        matchedVis = cv2.drawMatches(image, kpsA, template, kpsB, matches, None)
        matchedVis = imutils.resize(matchedVis, width=1000)
        #cv2.imshow("Matched Keypoints", matchedVis)
        #cv2.waitKey(0)

        # allocate memory for the keypoints (x,y-coordinates) from the
        # top matches -- we'll use these coordinates to compute our
        # homography matrix
        ptsA = np.zeros((len(matches), 2), dtype="float")
        ptsB = np.zeros((len(matches), 2), dtype="float")

        # loop over the top matches
        for (i, m) in enumerate(matches):
            # indicate that the two keypoints in the respective images
            # map to each other
            ptsA[i] = kpsA[m.queryIdx].pt
            ptsB[i] = kpsB[m.trainIdx].pt

        # compute the homography matrix between the two sets of matched
        # points
        (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)

        # use the homography matrix to align the images
        (h, w) = template.shape[:2]
        aligned = cv2.warpPerspective(image, H, (w, h))

        # write the aligned image
        #cv2.imshow("Aligned picture", aligned)
        #cv2.waitKey(0)
        cv2.imwrite('alignedImage.jpg', aligned)

    exit(0)


# main function
if __name__ == '__main__':
    main()
