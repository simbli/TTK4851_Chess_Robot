#File using the most common variables for easier tuning
CAMERA_CHANNEL = 0
CAMERA_SLEEP_TIME = 0.5
CHESSBOARD_SIZE = 8
INTERNAL_CORNERS = 7
MAT_SIZE = 9
EPSILON = 1e-9


#Parameters for initializing thresholding.
T_INIT = 90 
DT = 0.1


MEDIAN_MASK_SIZE = 3 #How large median filtering
GAUSSIAN_MASK_SIZE = 3 #How large gaussian blur filtering
COLOR_MEAN_MASK_SIZE = 5 #How large mask we use to find piece color
CUTOFF = 5 #How much of the corners of the squares are cut off
CANNY_LOWER = 35 #Lower threshold for canny edge detector
CANNY_HIGHER = 70 #Higher threshold for canny edge detector
W_MAX = 47 #Max width of contours to be accepted as pieces
W_MIN = 10 #Min width of contours to be accepted as pieces
H_MAX = 47 #Max heigth of contours to be accepted as pieces
H_MIN = 10 #Min heigth of contours to be accepted as pieces
