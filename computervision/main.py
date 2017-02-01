import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

def findContours(edges):
    contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours[1]

def printContours(image, contours):
    print 'found {} contours total'.format(len(contours))
    for c in contours:
#        (x,y,w,h) = cv2.boundingRect(c)
        cv2.drawContours(image, [c], -1,  (0,255,0),3)
        cv2.imshow('', image)
        cv2.waitKey(0)

def getCentroid(contour):
    M = cv2.moments(contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx, cy

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
    k = 7
    sharpeningKernelType = 1
    kernelSize = (k, k)

    
    #Open image with argv[1]
    filename = sys.argv[1]
    image = cv2.imread(filename, 0)
    show_picture(image, 'Original image')
    
    #Image-preprocessing to make edge detection easier
    image = cv2.GaussianBlur(image, kernelSize, 0)
    show_picture(image, 'Blurred with {}x{} gaussian kernel'.format(k,k))
    image = sharpen(image, sharpeningKernelType)
    show_picture(image, 'Sharpened image using kernel {}'.format(sharpeningKernelType)) 
    image = cv2.medianBlur(image, 7)
    image = cv2.GaussianBlur(image, kernelSize, 0)
    image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                                   cv2.THRESH_BINARY,11,2)
    image = cv2.GaussianBlur(image, kernelSize, 0)

    #Canny edge detection to find edges
    image = cv2.Canny(image, 0, 150, L2gradient=True)

    #Contour detection to find contours of pieces
#    contours = findContours(image)
#    printContours(image, contours)
    cv2.imshow('Edgedetection', image)
    cv2.waitKey(0)
