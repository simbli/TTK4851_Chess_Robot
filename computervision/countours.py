import cv2
import sys
import numpy as np
from main import sharpen

def getCentroid(contour):
    M = cv2.moments(contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx, cy

def morph_close(image):
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (40,40))
    closedImage = cv2.morphologyEx(image.copy(), cv2.MORPH_CLOSE, structuringElement)
    return closedImage

def morph_open(image):
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (40,40))
    openedImage = cv2.morphologyEx(image.copy(), cv2.MORPH_OPEN, structuringElement)
    return openedImage

#Read Image
image = cv2.imread(sys.argv[1], 1)
cv2.imshow('Original image', image)
cv2.waitKey(0)
#sharpen edges
#image = sharpen(image, 3)
#Smooth using a gaussian filter
blur = cv2.GaussianBlur(image, (5,5),0)
#Convert to Grayscale
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscaled image', gray)
cv2.waitKey(0)
#res1, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
#res2, thresh = cv2.threshold(gray, 150,255,cv2.THRESH_BINARY)
thresh = cv2.adaptiveThreshold(gray, 255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,19,2)
cv2.imshow('Tresholded image', thresh)
cv2.waitKey(0)
gray = cv2.medianBlur(thresh, 5)
cv2.imshow('median blurred', thresh)
cv2.waitKey(0)

#Should do some morphology on the thresholded image to enhance contours
#thresh = morph_open(thresh_inv)
#cv2.imshow('Closed image', thresh)
#cv2.waitKey(0)
#edges = cv2.Canny(thresh, 0, 180, L2gradient=True)
#cv2.imshow('Edges', edges)
#cv2.waitKey(0)
#Find edges

'''
#Find contours
contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0]
print 'Found {} contours'.format(len(contours))
#Print contours
#best_cnt = None
widths = []
heights = []
got_first_contour_loc = False
for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    #if True:
    if w < 50 and w > 20 and h < 50 and  h > 20:
        widths.append(w)
        heights.append(h)
        cv2.drawContours(image, [contour], -1, (0,255,0), 3)
        cv2.imshow("output", image)
        cv2.waitKey(0)

#avg_height = np.median(heights)
#avg_width = np.median(widths)
#print 'Average h: {} w: {}'.format(avg_height, avg_width)
#print 'First contour location is {},{}'.format(cx,cy)

#grid = getGrid(edges)
#cv2.imshow('grid', grid)
#cv2.waitKey(0)

#Crappy function with too much assumptions:
#idea: Assume that the first contour is the square on the bottom left. From there, Calculate the
#avg. gridsize for each square, and map each pixel to an according square.

chessboard = np.zeros((8,8))
#For each row
    #For each colums
        #Check if we have any contours with a centroid
            #If there is any, check the original black/white image in the same pos to see if it is a            #black or white piece
            #Mark the chessboard array with 1 or 2 if it is black or white

#import image
#blur
#Convert to Gray
#find contour to get board
#treshold the cut-out image
#Canny edge on cut-out
#Hough transform to find lines
#Detect if we have
'''
