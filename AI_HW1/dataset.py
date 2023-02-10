import os
import cv2
import numpy as np

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)

    '''
    Use os.listdir to get the path of face image and non-face image
    Read the image in gray scale by cv2.imread
    Form tuples with first element be the image, and the second be whether it is face or not(1 or 0)
    Append tuples into dataset list
    Return dataset list
    '''
    
    dataset = []
    faceImg = os.listdir(dataPath+'/face')
    nonFaceImg = os.listdir(dataPath+'/non-face')
    
    for img in faceImg:
      file = dataPath + '/face/' + img
      imgData = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
      dataset.append((imgData, 1))
    
    for img in nonFaceImg:
      file = dataPath + '/non-face/' + img
      imgData = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
      dataset.append((imgData, 0))
    # End your code (Part 1)
    
    
    return dataset
