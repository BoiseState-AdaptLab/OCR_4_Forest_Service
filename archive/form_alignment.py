#!/usr/bin/env python
# This script attempts to align an image to its corresponding template.
# Author: Sandra Busch
# Source: OCR with OpenCV, Tesseract, and Python
#   OCR Practitioner Bundle, 1st Edition (version 1.0)
#   Chapter 6 Image/Document Alignment and Registration
# Date: July 1, 2021

import os
import cv2
import numpy as np
import imutils


def main():
    image_path = None
    template_path = None
    max_features = 2000
    keep_percent = 0.2

    # prompt user for input
    if template_path != 'q' or image_path != 'q':
        template_path = input("Enter the path to the template or type q to quit: ")
        while not os.path.isfile(template_path):
            if template_path == 'q':
                exit(0)
            template_path = input("** The file could not be found ** \n Enter a valid path to the file: ")
        image_path = input("Enter the path to image being aligned or type q to quit: ")
        while not os.path.isfile(image_path):
            if image_path == 'q':
                exit(0)
            image_path = input("** The file could not be found ** \n Enter a valid path to the file: ")

        # open file as an image
        image = cv2.imread(image_path)
        template = cv2.imread(template_path)

        # align image and save it to file
        aligned = align_images(image, template, max_features, keep_percent)
        cv2.imwrite('alignedImage.jpg', aligned)

        # show image overlay to check accuracy of alignment
        output = overlay_images(aligned, template)
        cv2.imshow("Image Alignment Overlay", output)
        cv2.waitKey(0)


def align_images(image, template, max_features, keep_percent):
    # convert both the input image and template to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # use ORB to detect keypoints and extract (binary) local
    # invariant features
    orb = cv2.ORB_create(max_features)
    (kpsA, descsA) = orb.detectAndCompute(image_gray, None)
    (kpsB, descsB) = orb.detectAndCompute(template_gray, None)

    # match the features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)

    # sort the matches by their distance (the smaller the distance,
    # the "more similar" the features are)
    matches = sorted(matches, key=lambda x: x.distance)

    # keep only the top % of matches
    keep = int(len(matches) * keep_percent)
    matches = matches[:keep]

    # visualize the matched keypoints
    # uncomment this block to see the matched keypoints visualized
    # matchedVis = cv2.drawMatches(image, kpsA, template, kpsB, matches, None)
    # matchedVis = imutils.resize(matchedVis, width=1000)
    # cv2.imshow("Matched Keypoints", matchedVis)
    # cv2.waitKey(0)

    # allocate memory for the keypoints (x,y-coordinates) from the
    # top matches -- we'll use these coordinates to compute the
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

    # return the aligned image
    # cv2.imshow("Aligned picture", aligned)
    # cv2.waitKey(0)
    return aligned


def overlay_images(aligned, template):
    # resize both the aligned and template images so we can easily
    # visualize them on our screen
    aligned = imutils.resize(aligned, width=700)
    template = imutils.resize(template, width=700)

    # image alignment visualization will be *overlaying* the
    # aligned image on the template, that way we can obtain an idea of
    # how good our image alignment is
    overlay = template.copy()
    output = aligned.copy()
    cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
    return output


# main function
if __name__ == '__main__':
    main()
