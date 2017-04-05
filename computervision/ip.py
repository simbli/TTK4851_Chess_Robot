import sys
import cv2
from video import get_frame
import numpy as np
import math
import copy
import os.path
import matplotlib.pyplot as plt
import settings


def findSquareSize(corners):
    uppercorner = corners[0][0][1]
    lowercorner = corners[settings.INTERNAL_CORNERS - 1][0][1]
    return np.round(np.abs(uppercorner - lowercorner) / (settings.INTERNAL_CORNERS - 1))

def createBoardMatrix(frame):
    found, corners = cv2.findChessboardCorners(frame,(settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS))
    sorted_corners = sort_corners(corners)
    #order(frame, sorted_corners)
    midPixelIndex = 24
    midPixelX = corners[midPixelIndex][0][0]
    midPixelY = corners[midPixelIndex][0][1]

    startPixelX = corners[0][0][0]
    startPixelY = corners[0][0][1]

    squareSize = findSquareSize(sorted_corners)
    matSize = 9
    internalCorners = 7
    board = np.zeros((matSize,matSize,2))

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

    return board

def check_order(image, representation):
    for i in range(settings.MAT_SIZE):
        for j in range(settings.MAT_SIZE):
            cv2.circle(image,(np.int(representation[i][j][0]),np.int(representation[i][j][1])), 5, (0,0,255), -1)
            show_image(image)

def sort_corners(corners):
    centerPixelIndex = len(corners) / 2
    centerI = corners[centerPixelIndex][0][0]
    centerJ = corners[centerPixelIndex][0][1]

    startPixelIndex = 0
    startI = corners[startPixelIndex][0][0]
    startJ = corners[startPixelIndex][0][1]

    if startI < centerI:
        if startJ < centerJ:
            return hack_corners3(corners)
        else:
            return hack_corners2(corners)
    else:
        if startJ < centerJ:
            return hack_corners4(corners)
        else:
            return hack_corners1(corners)

def hack_corners1(corners):
    print "using hack_corners1"
    new_board = np.zeros((settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS,2))
    internalCorners = 7
    cornersLength = 48
    for i in range(internalCorners):
        for j in range(internalCorners):
            new_board[i, j, 0] = np.int(corners[cornersLength - (i * internalCorners + j)][0][0])
            new_board[i, j, 1] = np.int(corners[cornersLength - (i * internalCorners + j)][0][1])
    return new_board

#May need these functions

def hack_corners2(corners):
    print "using hack_corners2"
    new_board = np.zeros((settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS,2))
    internalCorners = 7
    cornersLength = 48
    for i in range(internalCorners):
        for j in range(internalCorners):
            new_board[i, j, 0] = np.int(corners[internalCorners*(j+1)-i-1][0][0])
            new_board[i, j, 1] = np.int(corners[internalCorners*(j+1)-i-1][0][1])
    return new_board

def hack_corners3(corners):
    print "using hack_corners3"
    new_board = np.zeros((settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS,2))
    internalCorners = 7
    cornersLength = 48
    for i in range(internalCorners):
        for j in range(internalCorners):
            new_board[i, j, 0] = np.int(corners[(i * internalCorners + j)][0][0])
            new_board[i, j, 1] = np.int(corners[(i * internalCorners + j)][0][1])
    return new_board


def hack_corners4(corners):
    print "using hack_corners4"
    new_board = np.zeros((settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS,2))
    internalCorners = 7
    cornersLength = 48
    for i in range(internalCorners):
        for j in range(internalCorners):
            new_board[i, j, 0] = np.int(corners[cornersLength - (internalCorners*(j+1)-i-1)][0][0])
            new_board[i, j, 1] = np.int(corners[cornersLength - (internalCorners*(j+1)-i-1)][0][1])
    return new_board

def draw_internal_corners(image, corners):
    for c in corners:
        cv2.drawChessboardCorners(image, (7,7), c, False)
        show_image(image)


def saveToFile(filename, boundaries):
    np.save(filename, boundaries)

def getFromFile(filename):
    return np.load(filename)

def calibrate(calib_frame=None):
    calibration_filename = 'computervision/boundaries.npy'
    if os.path.isfile(calibration_filename):
        print 'Calibration file found, using stored'
        return getFromFile(calibration_filename)
    else:
        calibrated = False
        while not calibrated:
            if calib_frame is None:
                frame = get_frame()
            else:
                frame = calib_frame
            found, corners = cv2.findChessboardCorners(frame, (7,7))
            try:
                cornersLength = len(corners)
            except:
                cornersLength = 0
            print 'Trying to calibrate, found {} of 49 internal corners'.format(cornersLength)

            if found and len(corners) == 49:
                calibrated = True
                boundaries = createBoardMatrix(frame)
        print 'Calibration complete, saving calibration file'
        saveToFile('computervision/boundaries', boundaries)
        return boundaries

def getCentroid(contour):
    M = cv2.moments(contour)
    cx = int(M['m10']/(M['m00'] + settings.EPSILON))
    cy = int(M['m01']/(M['m00'] + settings.EPSILON))
    return cx, cy

def find_color_mean(image):
    return np.mean(image)

def show_image(image):
    cv2.imshow('', image)
    cv2.waitKey(0)

def preprocess(image):
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (settings.GAUSSIAN_MASK_SIZE, settings.GAUSSIAN_MASK_SIZE),0)
    image = cv2.medianBlur(image, settings.MEDIAN_MASK_SIZE)
    return image


#This function will not work well with only white or black, but that is rarely the case
def calcThreshold(median_values):
    if len(median_values) != 0:
        median_max = np.max(median_values)
        median_min = np.min(median_values)
        print median_max
        print median_min
        midpoint = (median_max + median_min) / 2
        dt = settings.DT
        T_prev = 0
        T = midpoint
        while np.abs(T - T_prev) > dt:
            m1 = np.mean(median_values[median_values > T])
            m2 = np.mean(median_values[median_values <= T])
            T_prev = T
            T = (m1 + m2) / 2.0
        return T
    else:
        return 0

def classifyPieceColor(intensities, representation, th):
    for i in range(8):
        for j in range(8):
            if representation[i,j]:
                if intensities[i,j] <= th:
                    representation[i,j] = 2
                elif intensities[i,j] > th:
                    representation[i,j] = 1
                else:
                    print "what"

    return representation



def getRepresentation(image, boundaries):
    N_SQUARES = settings.CHESSBOARD_SIZE
    #Preprocess image as wholes
    image = preprocess(image)
    #Split image into 64 squares
    intensities = np.zeros((N_SQUARES, N_SQUARES))
    representation = np.zeros((N_SQUARES, N_SQUARES))
    #get if there is a piece in the square and what the median/mean intensity of the middle is
    median_list = []
    for i in range(N_SQUARES):
        for j in range(N_SQUARES):
            square = getCroppedSquare(image, boundaries, i, j)
            isPiece, medianVal = findChessPieceInSquare(square)
            if isPiece:
                intensities[i,j] = medianVal
                representation[i,j] = True
                median_list.append(medianVal)

    median_list = np.asarray(median_list)
    th = calcThreshold(median_list)
    representation = classifyPieceColor(intensities, representation, th)
    return representation

def getCroppedSquare(image, boundaries, row, col):
    cutoff = settings.CUTOFF
    torow = int(max(boundaries[row][col][0], boundaries[row][col+1][0])) - cutoff
    fromrow = int(min(boundaries[row+1][col][0], boundaries[row+1][col+1][0])) + cutoff
    tocol = int(max(boundaries[row][col][1], boundaries[row+1][col][1])) - cutoff
    fromcol = int(min(boundaries[row][col+1][1], boundaries[row+1][col+1][1])) + cutoff
    cropped = image[fromcol:tocol, fromrow:torow]
    return cropped

def findChessPieceInSquare(square_image):

    canny = cv2.Canny(square_image, settings.CANNY_LOWER, settings.CANNY_HIGHER)#, L2gradient=True)
    contours = cv2.findContours(canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    i = 0
    size = settings.COLOR_MEAN_MASK_SIZE
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        i+=1
        #Check if contour is right size
        if w < settings.W_MAX and w > settings.W_MIN and h < settings.H_MAX and h > settings.H_MIN:
            cx = np.round(square_image.shape[0]/2)
            cy = np.round(square_image.shape[1]/2)
            l = []
            #Check neighbourhood to get median value of middle of square
            for j in range(-(size-1)/2,(size-1)/2 + 1):
                for k in range(-(size-1)/2,(size-1)/2 + 1):
                    try:
                        val = square_image[cx+j,cy+k]
                        l.append(val)
                    except:
                        pass
            median_val = np.median(l)
            return True, median_val
    if i != 1 or 2:
        return False, None

def openAndInitializeImage(filename):
    image = cv2.imread(filename, 1)
    #image = cv2.GaussianBlur(image, (7,7),0)
    #image = cv2.medianBlur(image, 7)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

if __name__ == '__main__':
    #Usage: python <calibrationimage> <image_to_be_checked>

    calibration_image_filename = sys.argv[1]
    chessboard_image_filename = sys.argv[2]
    calibration_image = openAndInitializeImage(calibration_image_filename)
    chessboard_image = openAndInitializeImage(chessboard_image_filename)
    boundaries = calibrate(calibration_image)

    res = getRepresentation(chessboard_image, boundaries)
    try:
        from plot import plot_array
        plot_array(res)
    except:
        print res
