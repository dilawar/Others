"""locate_mouse.py: 

Locate stupid mouse in video.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh "
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import glob

import dlib
from skimage import io
import imageio
import cv2

bbox_ = None
current_frame_ = None

def onmouse(event, x, y, flags, params):
    global current_frame_, bbox_
    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox_ = []
        bbox_.append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        bbox_.append((x, y))
        cv2.rectangle(current_frame_, bbox_[0], (x,y), 0,2)


def get_rectangle( frame ):
    global bbox_
    global current_frame_
    current_frame_ = frame.copy()
    title = "Bound head and press 'q' to quit."
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, onmouse)
    clone = frame.copy()
    while True:
        cv2.imshow(title, current_frame_)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            current_frame_ = clone.copy()
        elif key == ord("q"):
            break
    cv2.waitKey(1)
    cv2.destroyWindow( title )
    return bbox_


def main():
    videofile = sys.argv[1]
    print('[INFO] Reading %s' % videofile )
    vid = imageio.get_reader( videofile )
    nFrames = 0
    frames = []
    for i in range(1000, 3000):
        img = vid.get_data( i )
        frames.append( img )
        nFrames += 1
    print('[INFO] Loaded all frames' )

    bbox_ = get_rectangle( frames[0] )
    # Create the correlation tracker - the object needs to be initialized
    # before it can be used
    tracker = dlib.correlation_tracker()

    win = dlib.image_window()
    # We will track the frames as we load them off of disk

    for k, img in enumerate(frames):
        print("Processing Frame {}".format(k))
        # We need to initialize the tracker on the first frame
        if k == 0:
            # Start a track on the juice box. If you look at the first frame you
            # will see that the juice box is contained within the bounding
            # box (74, 67, 112, 153).
            (x0, y0), (x1, y1) = bbox_
            tracker.start_track(img, dlib.rectangle( x0, y0, x1, y1 ))
        else:
            # Else we just attempt to track from the previous frame
            tracker.update(img)

        win.clear_overlay()
        win.set_image(img)
        win.add_overlay(tracker.get_position())
        # dlib.hit_enter_to_continue()

if __name__ == '__main__':
    main()
