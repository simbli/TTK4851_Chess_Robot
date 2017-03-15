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


def getGrid(edges, th=140, original_image=None, show_on_image=False):
    grid = np.zeros(edges.shape)
    lines = cv2.HoughLines(edges.copy(), 1, np.pi/180, th)
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*a)
            x2 = int(x0 -1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(grid, (x1, y1), (x2, y2), (255), 2)
            if show_on_image:
                cv2.line(original_image, (x1,y1), (x2,y2), (255), 2)

    if show_on_image:
        show_picture(original_image, 'Lines on original image')
    return grid

def getGrid2(edges, th, original_image=None, show_on_image=False):
    grid = np.zeros(edges.shape)
    lines = cv2.HoughLinesP(edges.copy(), 1, np.pi/180, th, minLineLength=300, maxLineGap=20)
    for x1, x2, y1, y2 in lines[0]:
        cv2.line(grid, (x1,x2), (y1,y2), (255), 2)
        if show_on_image:
            cv2.line(original_image, (x1,x2), (y1,y2), (255), 2)

    if show_on_image:
        show_picture(original_image, 'Lines on image')
    return grid

def findGridSize(grid):
    width = []
    height = []
    c_w = 0
    c_h = 0
    for i in range(grid.shape[1]):
        if grid[0,i] != 255:
            c_w += 1
        else:
            if c_w > 3:
                width.append(c_w)
            c_w = 0
    width.append(c_w)

    for j in range(grid.shape[0]):
        if grid[j, 0] != 255:
            c_h += 1
        else:
            if c_h > 3:
                height.append(c_h)
            c_h = 0
    height.append(c_h)
    
    cols = len(width)
    rows = len(height)
    avg_cols_size = int(np.mean(width))
    avg_rows_size = int(np.mean(height))
    print 'The image has {} rows and {} cols width an average rowsize {} and colsize {}'.format(rows, cols, avg_rows_size, avg_cols_size)
    return (rows, cols), (avg_rows_size, avg_cols_size)

        
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
    k = 3
    sharpeningKernelType = 1
    kernelSize = (k, k)

    
    #Open image with argv[1]
    filename = sys.argv[1]
    original_image = cv2.imread(filename, 0)
    show_picture(original_image, 'Original image')
    image = original_image.copy()
    #Image-preprocessing to make edge detection easier
    image = cv2.GaussianBlur(image, kernelSize, 0)
    show_picture(image, 'Blurred with {}x{} gaussian kernel'.format(k,k))
    #image = sharpen(image, sharpeningKernelType)
    #show_picture(image, 'Sharpened image using kernel {}'.format(sharpeningKernelType)) 
    #image = cv2.medianBlur(image, 7)
    #image = cv2.GaussianBlur(image, kernelSize, 0)
    #image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #                                               cv2.THRESH_BINARY,11,2)
    #show_picture(image, 'Adaptive tresholded image')
    #image = cv2.GaussianBlur(image, kernelSize, 0)

    #Canny edge detection to find edges
    image = cv2.Canny(image, 0, 140, L2gradient=True)
    show_picture(image, 'Edge detection')
    #Hough transform to get lines of the board
    grid = getGrid2(image, th=50, original_image=original_image.copy(), show_on_image=True)
    show_picture(grid, 'Hough transform')
    size = findGridSize(grid)
    #Contour detection to find contours of pieces
    contours = findContours(image)
    printContours(image, contours)
    cv2.waitKey(0)
