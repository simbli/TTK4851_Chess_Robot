import cv2
import sys
from video import get_frame
import numpy as np

#image = get_frame()
filename = sys.argv[1]
image = cv2.imread(filename, 1)
#cv2.imshow('original', image)
#cv2.waitKey(0)
num_corners = (7,7)

#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#This finds corners on empty boards, but fails on full boards
#May be able as long as we get more than N corners, we can calculate
#on the assumption that the coordinates is linear tho they are not
#need to find documentation on what order they find it

#(h, w) = image.shape[:2]
#center = (w / 2, h / 2)
#M = cv2.getRotationMatrix2D(center, -90, 1.0)
# image = cv2.warpAffine(image, M, (w, h))
#cv2.imshow('asdf', image)
#cv2.waitKey(0)


found, corners = cv2.findChessboardCorners(image, (7,7))#, flags=cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH)
print found
internalCorners = 7
#for c in corners:
cv2.drawChessboardCorners(image, (7,7), corners[internalCorners * 6], False)
#cv2.imshow('chessboardcorners', image)
#cv2.waitKey(0)
#cv2.drawChessboardCorners(image, (7,7), corners[7], False)
#cv2.imshow('chessboardcorners', image)
#cv2.waitKey(0)
print type(corners)

uppercorner = corners[0][0][1]
lowercorner = corners[6][0][1]



def findSquareSize(frame, corners):
    uppercorner = corners[0][0][1]
    lowercorner = corners[6][0][1]
    return np.round(np.abs(uppercorner - lowercorner) / 6)

def createBoardMatrix(frame):
    found, corners = cv2.findChessboardCorners(image,(7,7))#, flags=cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH)
    squareSize = findSquareSize(frame, corners)
    matSize = 9
    board = np.zeros((9,9,2))

    #upper left
    for i in range(2):
        board[0][0][i] = np.round(corners[internalCorners * (internalCorners - 1)][0][i] - squareSize)
    #lower left
    for i in range(2):
        board[matSize - 1][0][i] = np.round(corners[internalCorners * internalCorners - 1][0][i] - squareSize*(-1)**i)

    #upper right
    for i in range(2):
        board[0][matSize - 1][i] = np.round(corners[0][0][i] - squareSize*(-1)**(i+1))

    #lower right
    for i in range(2):
        board[matSize - 1][matSize - 1][i] = np.round(corners[internalCorners - 1][0][i] + squareSize)

    #Upper row
    for i in range(1, matSize - 1):
        board[0][i][0] = np.round(corners[internalCorners * (internalCorners - i)][0][0])
        board[0][i][1] = np.round(corners[internalCorners * (internalCorners - i)][0][1] - squareSize)

    #bottom row
    for i in range(1, matSize - 1):
        board[matSize - 1][i][0] = np.round(corners[internalCorners * (internalCorners - i + 1) - 1][0][0])
        board[matSize - 1][i][1] = np.round(corners[internalCorners * (internalCorners - i + 1) - 1][0][1] + squareSize)

    #left column
    for i in range(1, matSize - 1):
        cornerIndex = internalCorners * (internalCorners - 1) + i - 1
        board[i][0][0] = np.round(corners[cornerIndex][0][0] - squareSize)
        board[i][0][1] = np.round(corners[cornerIndex][0][1])

    #right column
    for i in range(1, matSize - 1):
        cornerIndex = i - 1
        board[i][matSize - 1][0] = np.round(corners[cornerIndex][0][0] + squareSize)
        board[i][matSize - 1][1] = np.round(corners[cornerIndex][0][1])

    #internal corners
    for i in range(1, matSize-1):
        for j in range(1, matSize-1):
            cornerIndex = internalCorners * (internalCorners - j) + i - 1
            board[i][j][0] = np.round(corners[cornerIndex][0][0])
            board[i][j][1] = np.round(corners[cornerIndex][0][1])

    print board

def print_corner(image, board):
    cv2.drawChessboardCorners(image, (7,7), board, False)
    cv2.imshow('Drawn corner', image)
    cv2.waitKey(0)

"""
def calibrate():
    calibrated = False
    while not calibrated:
        print 'Starting calibration iteration'
        frame = get_frame()
        found, corners = cv2.findChessboardCorners(frame, (7,7))#, flags=cv2.cv.CV_CALIB_CB_ADAPTIVE_THRESH)
        if found and len(corners) == 49:
            calibrated = True
    print 'Calibration complete'
"""

if __name__ == '__main__':
    createBoardMatrix(image)
#    calibrate()
