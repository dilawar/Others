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



def main():
    videofile = sys.argv[1]
    print('[INFO] Reading %s' % videofile )
    vid = imageio.get_reader( videofile )
    nFrames = 0
    frames = []
    for i in range(2000, 3000):
        img = vid.get_data( i )
        frames.append( img )
        nFrames += 1
    print('[INFO] Loaded all frames' )

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
            tracker.start_track(img, dlib.rectangle(354, 347, 412, 553))
        else:
            # Else we just attempt to track from the previous frame
            tracker.update(img)

        win.clear_overlay()
        win.set_image(img)
        win.add_overlay(tracker.get_position())
        # dlib.hit_enter_to_continue()

if __name__ == '__main__':
    main()
