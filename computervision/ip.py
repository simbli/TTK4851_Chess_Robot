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
    #draw_internal_corners(frame.copy(), corners)
    sorted_corners = sort_corners(corners)
    #check_order(frame, sorted_corners)
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
            return hack_corners4(corners)
    else:
        if startJ < centerJ:
            return hack_corners2(corners)
        else:
            return hack_corners1(corners)

def hack_corners1(corners):
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
    new_board = np.zeros((settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS,2))
    internalCorners = 7
    cornersLength = 48
    for i in range(internalCorners):
        for j in range(internalCorners):
            new_board[i, j, 0] = np.int(corners[internalCorners*(j+1)-i-1][0][0])
            new_board[i, j, 1] = np.int(corners[internalCorners*(j+1)-i-1][0][1])
    return new_board

def hack_corners3(corners):
    new_board = np.zeros((settings.INTERNAL_CORNERS,settings.INTERNAL_CORNERS,2))
    internalCorners = 7
    cornersLength = 48
    for i in range(internalCorners):
        for j in range(internalCorners):
            new_board[i, j, 0] = np.int(corners[(i * internalCorners + j)][0][0])
            new_board[i, j, 1] = np.int(corners[(i * internalCorners + j)][0][1])
    return new_board


def hack_corners4(corners):
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

def removeIntensities(image, th):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] > th:
                image[i,j] = th


def saveBoundariesToFile(filename, boundaries):
    np.save(filename, boundaries)

def getBoundariesFromFile(filename):
    return np.load(filename)

def calibrate():
    calibration_filename = 'computervision/boundaries.npy'
    if os.path.isfile(calibration_filename):
        print 'Calibration file found, using stored'
        return getBoundariesFromFile(calibration_filename)
    else:
        calibrated = False
        while not calibrated:
            frame = get_frame()
            found, corners = cv2.findChessboardCorners(frame, (7,7))#, flags=cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH)
            try:
                cornersLength = len(corners)
            except:
                cornersLength = 0

            if cornersLength == 0:
                print 'Trying to calibrate, found {} of 64 corners'.format(cornersLength)
            else:
                print 'Trying to calibrate, found {} of 64 corners'.format(cornersLength + 15)

            if found and len(corners) == 49:
                calibrated = True
                boundaries = createBoardMatrix(frame)
        print 'Calibration complete, saving calibration file'
        saveBoundariesToFile('computervision/boundaries', boundaries)
        return boundaries

def getCentroid(contour):
    M = cv2.moments(contour)
    cx = int(M['m10']/(M['m00'] + settings.EPSILON))
    cy = int(M['m01']/(M['m00'] + settings.EPSILON))
    return cx, cy

def checkSquareForContours(image, board, row, col,):
    cutoff = settings.CUTOFF
    torow = int(max(board[row][col][0], board[row][col+1][0])) - cutoff
    fromrow = int(min(board[row+1][col][0], board[row+1][col+1][0])) + cutoff

    tocol = int(max(board[row][col][1], board[row+1][col][1])) - cutoff
    fromcol = int(min(board[row][col+1][1], board[row+1][col+1][1])) + cutoff
    cropped = image[fromcol:tocol, fromrow:torow]
    res = findContour(cropped, row, col)
    return res

def find_color_mean(image):
    return np.mean(image)

def show_image(image):
    cv2.imshow('', image)
    cv2.waitKey(0)

def findChesspieceColor(image, contours, row, col):
    img2 = image.copy()
    i = 0
    size = settings.COLOR_MEAN_MASK_SIZE
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        i+=1
        if w < settings.W_MAX and w > settings.W_MIN and h < settings.H_MAX and h > settings.H_MIN:
            cx, cy = getCentroid(contour)
            l = []
            for j in range(-(size-1)/2,(size-1)/2 + 1):
                for k in range(-(size-1)/2,(size-1)/2 + 1):
                    #cv2.drawContours(img2, contour, -1, (0,255,0), 3)
                    #show_image(img2)
                    try:
                        val = image[cx+j,cy+k]
                        l.append(val)
                    except:
                        pass
            mean_val = np.mean(l)
            median_val = np.median(l)
            if median_val < settings.TH_BLACK_WHITE:
                return 2
            else:
                return 1
    if i != 1 or 2:
        return 0

def getHist(image):
    vals = image.mean(axis=2).flatten()
    # plot histogram with 255 bins
    b, bins, patches = plt.hist(vals, 255)
    plt.xlim([0,255])
    plt.show()

def preprocess(image):
    #th = 200
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #removeIntensities(image, th)
    image = cv2.GaussianBlur(image, (settings.GAUSSIAN_MASK_SIZE, settings.GAUSSIAN_MASK_SIZE),0)
    image = cv2.medianBlur(image, settings.MEDIAN_MASK_SIZE)
    return image


def findContour(image, row, col):
    #show_image(image)
    canny = cv2.Canny(image, settings.CANNY_LOWER, settings.CANNY_HIGHER)#, L2gradient=True)
    contours = cv2.findContours(canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    return findChesspieceColor(image, contours, row, col)

def getRepresentation(boundaries, image):
    N_SQUARES = settings.CHESSBOARD_SIZE
    #Move preprocessing on each square

    image = preprocess(image)
    mat = np.zeros((N_SQUARES,N_SQUARES))
    for i in range(N_SQUARES):
        for j in range(N_SQUARES):
            mat[i,j] = checkSquareForContours(image, boundaries, i, j)
    return mat

def get_threshold(image, contours):
    white_list = []
    black_list = []
    for i in range(2):
        for j in range(8):
            black_list.append(get_median(image, contours, i, j))

    for i in range(6,8):
        for j in range(8):
            white_list.append(get_median(image, contours, i, j))

    thresh = np.median(white_list - black_list) / 2
    print "Optimal threshold is: {}".format(thresh)
    return thresh

def openAndInitializeImage(filename):
    image = cv2.imread(filename, 1)
    image = cv2.GaussianBlur(image, (7,7),0)
    image = cv2.medianBlur(image, 7)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

if __name__ == '__main__':
    #Usage: python <calibrationimage> <image_to_be_checked>

    calibration_image_filename = sys.argv[1]
    chessboard_image_filename = sys.argv[2]
    calibration_image = openAndInitializeImage(calibration_image_filename)
    chessboard_image = openAndInitializeImage(chessboard_image_filename)
    boundaries = calibrate(calibration_image)

    res = getRepresentation(boundaries, chessboard_image)
    try:
        from plot import plot_array
        plot_array(res)
    except:
        print res
