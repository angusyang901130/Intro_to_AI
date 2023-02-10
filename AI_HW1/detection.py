import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """         
    
    # Begin your code (Part 4)

    '''
    Read detectData.txt
    When read the line contains only two elements, first: image name, second: number
    Than read the image and run a loop to find the part we need to classify
    Each loop read the range we want classify
    Loop size is the second element of the line only contain two elements

    Read the image in gray and original color
    Gray image is used for detecting, original image is used for drawing rectangle

    For gray image:
      Cut the image to the size that we want to classify whether it is a face
      Resize to 19 x 19 to meet the shape of the training data
      Use clf.classify(the resized image) to detect whether it is a face
    
    For normal image:
      After classified, draw green rectangle if it is a face, red if not a face
      Show the result using imshow
      Use cv2.waiKey() to present result of each image
    '''

    text = open(dataPath, encoding="utf-8").readlines()
    for i in range(len(text)):
      text[i] = text[i].replace('\n', '')
      text[i] = text[i].split(' ')
    
    for i in range(len(text)):
      if len(text[i]) == 2:
        count = int(text[i][1])
        grayImage = cv2.imread('data/detect/' + text[i][0], cv2.IMREAD_GRAYSCALE)
        image = cv2.imread('data/detect/' + text[i][0])

        for j in range(i+1, i+count+1):
          for t in range(len(text[j])):
            text[j][t] = int(text[j][t])
          x, y, width, height = text[j]
          img = grayImage[y:y+height, x:x+width]

          img = cv2.resize(img, (19, 19), interpolation=cv2.INTER_NEAREST)
          start = (x, y)
          end = (x+width, y+height)
          if clf.classify(img):
            image = cv2.rectangle(image, start, end, (0, 255, 0), thickness=2)
          else:
            image = cv2.rectangle(image, start, end, (0, 0, 255), thickness=2)
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow("image", image)
        cv2.waitKey()
          

    # End your code (Part 4)
