import sys
import cv2
from video import get_frame
import numpy as np
import math
import copy
import os.path
#image = get_frame()

#def get_frame():
#    return cv2.imread(sys.argv[1],1)


def findSquareSize(corners):
    uppercorner = corners[0][0][1]
    lowercorner = corners[6][0][1]
    return np.round(np.abs(uppercorner - lowercorner) / 6)


def sortCorners(corners):
    new_corners = np.zeros((7,7,2))
    squareSize = findSquareSize(corners)

    min_corner = 0
    min_x = corners[0][0][0]
    min_y = corners[0][0][1]
    error = squareSize/2
    for i in range(1,len(corners)):
        foundMin = False
        temp_corner = i
        temp_x = corners[i][0][0]
        temp_y = corners[i][0][1]
        if temp_x < min_x - error:
            if (temp_y < min_y + error):
                foundMin = True
        elif temp_x < min_x + error:
            if (temp_y < min_y - error):
                foundMin = True

        if foundMin:
            min_x = temp_x
            min_y = temp_y
            min_corner = temp_corner

    new_corners[0][0][0] = corners[min_corner][0][0]
    new_corners[0][0][1] = corners[min_corner][0][1]

    for i in range(len(new_corners)):
        row = new_corners[i]
        for g in range(len(row)):
            foundCorner = False
            x = 0
            y = 0
            if (g == 0):
                if (i == 0):
                    foundCorner = True
                else:
                    x = new_corners[i-1][g][0]
                    y = new_corners[i-1][g][1]+squareSize
            else:
                x = new_corners[i][g-1][0]+squareSize
                y = new_corners[i][g-1][1]

            index = 0
            while not foundCorner and index < len(corners):
                corner = corners[index]
                cornerx = corner[0][0]
                cornery = corner[0][1]
                if (np.abs(cornerx-x) < error):
                    if (np.abs(cornery-y) < error):
                        foundCorner = True
                        new_corners[i][g][0] = cornerx
                        new_corners[i][g][1] = cornery

                index += 1
            if (not foundCorner):
                print "i = {}, g = {}. couldnt sort corners because couldnt find corner".format(i,g)
    return new_corners

def saveBoundariesToFile(filename, boundaries):
    np.save(filename, boundaries)

def getBoundariesFromFile(filename='boundaries.npy'):
    return np.load(filename)


def createBoardMatrix(frame):
    found, corners = cv2.findChessboardCorners(frame,(7,7))
    sorted_corners = sortCorners(corners)
    midPixelIndex = 24
    midPixelX = corners[midPixelIndex][0][0]
    midPixelY = corners[midPixelIndex][0][1]

    startPixelX = corners[0][0][0]
    startPixelY = corners[0][0][1]

    squareSize = findSquareSize(corners)
    matSize = 9
    internalCorners = 7
    board = np.zeros((9,9,2))

    #upper left
    for i in range(2):
        board[0][0][i] = np.round(sorted_corners[0][0][i] - squareSize)

    #Lower left
    for i in range(2):
        board[matSize - 1][0][i] = np.round(sorted_corners[internalCorners - 1][0][i] - squareSize*(-1)**i)

    #upper right
    for i in range(2):
        board[0][matSize - 1][i] = np.round(sorted_corners[0][internalCorners -1][i] - squareSize *(-1)**(i+1))

    #lower right
    for i in range(2):
        board[matSize - 1][matSize - 1][i] = np.round(sorted_corners[internalCorners-1][internalCorners-1][i] + squareSize)

    #top row
    for i in range(1, matSize - 1):
        board[0][i][0] = np.round(sorted_corners[0][i-1][0])
        board[0][i][1] = np.round(sorted_corners[0][i-1][1] - squareSize)

    #bottom row
    for i in range(1, matSize - 1):
        board[matSize - 1][i][0] = np.round(sorted_corners[internalCorners-1][i-1][0])
        board[matSize - 1][i][1] = np.round(sorted_corners[internalCorners-1][i-1][1] + squareSize)

    #left column
    for i in range(1, matSize - 1):
        board[i][0][0] = np.round(sorted_corners[i-1][0][0] - squareSize)
        board[i][0][1] = np.round(sorted_corners[i-1][0][1])

    #right column
    for i in range(1, matSize - 1):
        board[i][matSize - 1][0] = np.round(sorted_corners[i-1][internalCorners-1][0] + squareSize)
        board[i][matSize - 1][1] = np.round(sorted_corners[i-1][internalCorners-1][1])

    #internal corners
    for i in range(1, matSize-1):
        for j in range(1, matSize-1):
            board[i][j][0] = np.round(sorted_corners[i-1][j-1][0])
            board[i][j][1] = np.round(sorted_corners[i-1][j-1][1])

    #print board
    return board

def print_corner(image, board):
    cv2.drawChessboardCorners(image, (7,7), board, False)
    cv2.imshow('Drawn corner', image)
    cv2.waitKey(0)


def calibrate(frame=None):
    calibration_filename = 'boundaries.npy'
    if os.path.isfile(calibration_filename):
        print 'Calibration file found, using stored'
        return getBoundariesFromFile(calibration_filename)
    else:
        calibrated = False
        while not calibrated:
            print 'Trying to calibrate'
            if frame is None:
                frame = get_frame()
            found, corners = cv2.findChessboardCorners(frame, (7,7))#, flags=cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH)
            if found and len(corners) == 49:
                calibrated = True
                boundaries = createBoardMatrix(frame)
        print 'Calibration complete, saving calibration file'
        saveBoundariesToFile('boundaries', boundaries)
        return boundaries

def getCentroid(contour):
    M = cv2.moments(contour)
    cx = int(M['m10']/(M['m00'] + 1e-9))
    cy = int(M['m01']/(M['m00'] + 1e-9))
    return cx, cy

def checkSquareForContours(image, board, row, col):
    torow = int(max(board[row][col][0], board[row][col+1][0]))
    fromrow = int(min(board[row+1][col][0], board[row+1][col+1][0]))

    tocol = int(max(board[row][col][1], board[row+1][col][1]))
    fromcol = int(min(board[row][col+1][1], board[row+1][col+1][1]))
    cropped = image[fromcol:tocol, fromrow:torow]
    res = findContour(cropped)
    return res

def show_image(image):
    cv2.imshow('', image)
    cv2.waitKey(0)

def findContour(image):
    #show_image(image)
    TH_BLACK_WHITE = 70 #Threshold of color intesity to separate white from black pieces
    #Find optimal thresholding algorithm
    #res1, thresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    #res2, thresh = cv2.threshold(gray, 150,255,cv2.THRESH_BINARY)
    #thresh = cv2.adaptiveThreshold(image, 255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,19,2)
    canny = cv2.Canny(image, 200, 250)#, L2gradient=True)
    contours = cv2.findContours(canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    i = 0
    #show_image(canny)

    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        #print 'width/height = {},{}'.format(w,h)
        if w < 47 and w > 10 and h < 47 and  h > 10: #Compute these values instead of hardcode them
            i += 1
            cx, cy = getCentroid(contour)
            l = []
            for j in range(-1,2):
                for k in range(-1,2):
                    try:
                        val = image[cx+j,cy+k]
                        l.append(val)
                    except:
                        pass
            mean_val = np.mean(l)
            #print 'Value of centroid pixel is: {}'.format(val)
            #print 'Mean of 3x3 centroid is: {}'.format(mean_val)
            if mean_val < TH_BLACK_WHITE:
                return 2
            else:
                return 1
    if i != 1 or 2:
        return 0

def getRepresentation(boundaries, image, N_SQUARES=8):
    mat = np.zeros((N_SQUARES,N_SQUARES))
    for i in range(N_SQUARES):
        for j in range(N_SQUARES):
            mat[i,j] = checkSquareForContours(image, boundaries, i, j)
    return mat

def openAndInitializeImage(filename):
    image = cv2.imread(filename, 1)
    image = cv2.GaussianBlur(image, (5,5),0)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

if __name__ == '__main__':
    calibration_image_filename = sys.argv[1]
    chessboard_image_filename = sys.argv[2]
    calibration_image = openAndInitializeImage(calibration_image_filename)
    chessboard_image = openAndInitializeImage(chessboard_image_filename)

    boundaries = calibrate(calibration_image)
    res = getRepresentation(boundaries, chessboard_image)
    print res
