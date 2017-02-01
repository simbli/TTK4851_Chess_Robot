import cv2
import numpy as np
import pygame

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

def start_video_stream(grayScale=True, sound=False):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if grayScale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

def take_snapshot(grayScale=True, sound=False):
    cap= cv2.VideoCapture(0)
    ret, frame = cap.read()
    if grayScale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('SNAPSHOT', frame)

    play_sound('click.wav')
    save_image(frame)
    cv2.waitKey(0)
    
if __name__ == '__main__':
    start_video_stream(False)
    #take_snapshot()
