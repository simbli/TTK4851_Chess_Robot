import cv2
import numpy as np
import pygame
import sys

#Sets up videostream from video source 0.
#Press s to take snapshot
#Press q to quit

def play_sound(filename):
    pygame.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


def save_image(frame):

    random_integer = np.random.randint(100000)
    filename = 'images/snapshot' + str(random_integer) + '.png'

    try:
        cv2.imwrite(filename, frame)
        print 'Writing file: {}'.format(filename)
    except:
        print 'Could not write file'

"""
def start_video_stream(grayScale=True, sound=False):

    play_sound('click.wav')
    random_integer = np.random.randint(100000)
    filename = 'images/snapshot' + str(random_integer) + '.png'
    print 'Writing file: {}'.format(filename)
    cv2.imwrite(filename, frame)
"""

def capture_video(output_filename):
    cap = cv2.VideoCapture(1)

    # Define the codec and create VideoWriter object
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = output_filename + '.avi'
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter(filename,fourcc, 20.0, (640,480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            #frame = cv2.flip(frame,0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def start_video_stream(grayScale=False, sound=False):

    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if grayScale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame,-1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):

            if sound:
                play_sound('click.wav')

            cv2.imshow('Snapshot', frame)
            save_image(frame)
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pass


def get_frame(grayScale=False):
    cap= cv2.VideoCapture(1)
    ret, frame = cap.read()
    frame = cv2.flip(frame,-1)
    if grayScale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cap.release()
    cv2.destroyAllWindows()
    return frame

if __name__ == '__main__':
    #filename = sys.argv[1]
    start_video_stream()
    #capture_video(filename)
