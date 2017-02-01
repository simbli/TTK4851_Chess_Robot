import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys


def histogramEqualization(image, plot=False):
    equ = cv2.equalizeHist(image)
    if plot:
        plt.hist(image.ravel(),256,[0,256]); plt.show()
        plt.hist(equ.ravel(),256,[0,256]); plt.show()
    return equ

def show_picture(image, title=''):
    cv2.imshow(title, image)
    cv2.waitKey(0)

def canny(img):
    edges = cv2.Canny(img, 0, 150, L2gradient=True)
    show_picture(edges)
    
def sharpen(img, k):
    if k == 1:
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    elif k == 2:
        kernel = np.array([[1,1,1], [1,-7,1], [1,1,1]])
    elif k == 3:
        kernel = np.array([[-1,-1,-1,-1,-1],
                                 [-1,2,2,2,-1],
                                 [-1,2,8,2,-1],
                                 [-1,2,2,2,-1],
                                 [-1,-1,-1,-1,-1]]) / 8.0


    output = cv2.filter2D(img, -1, kernel)
    show_picture(output, 'kernel' + str(k))
    return output
    
if __name__ == '__main__':
    kernelSize = 7
    kernelSize = (kernelSize, kernelSize)
    filename = sys.argv[1]

    image = cv2.imread(filename, 0)
    image = cv2.GaussianBlur(image, kernelSize, 0)
    image = sharpen(image, 1)
    image = cv2.medianBlur(image, 7)
    
    image = cv2.GaussianBlur(image, kernelSize, 0)
    image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                                   cv2.THRESH_BINARY,11,2)

    image = cv2.GaussianBlur(image, kernelSize, 0)
    image = cv2.Canny(image, 0, 150, L2gradient=True)
    cv2.imshow('Edgedetection', image)
    cv2.waitKey(0)
