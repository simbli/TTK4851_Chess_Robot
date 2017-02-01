import cv2
import numpy as np


#Sets up videostream from video source 0.
#Press s to take snapshot
#Press q to quit 

def save_image(frame):
    random_integer = np.random.randint(100000)
    filename = 'images/snapshot' + str(random_integer) + '.png'
    print 'Writing file: {}'.format(filename)
    cv2.imwrite(filename, frame)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imshow('Snapshot', gray)
            save_image(gray)
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    pass
