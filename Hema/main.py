"""main.py: 

"""

from __future__ import print_function
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pickle
import os
import sys
import cv2
import detect_honeybees as hb
from collections import defaultdict

args_ = None 

nframes_ = 0
avg_ = None
frames_ = [ ]

user_defined_points_ = [ ]
rois_ = [ ]

# Callback functions.
drawing = False
mode = True
ix, iy = -1, -1
current_frame_ = None

# Store data in this dict.
data_ = defaultdict( list )

def draw_ellipse_roi(event, x, y, flags, param):
    global ix,iy,drawing,mode
    global user_defined_points_

    if event == cv2.EVENT_LBUTTONDOWN:
        user_defined_points_.append( (x,y) )

    elif event == cv2.EVENT_RBUTTONUP:
        # Added ellipse.
        if len( user_defined_points_ ) > 4:
            rois_.append( cv2.fitEllipse( np.array( user_defined_points_) ) )
        user_defined_points_ = [ ]


cv2.namedWindow( 'main' )
cv2.setMouseCallback( 'main', draw_ellipse_roi )

def get_signal( img, el ):
    p1, p2, theta = el
    if p1 > p2:
        p2, p1 = p1, p2
    x1, y1 = p1
    x2, y2 = p2
    return np.mean( img[int(x1):int(x2),int(y1):int(y2)] )

def show_image( img = None, img2 = None, waitFor = 1 ):
    global current_frame_ 
    global rois_
    global data_

    if img is None:
        img = current_frame_
    if img2 is not None:
        img = np.vstack( [img, img2] )

    # Draw all ellipse.
    for el in rois_:
        cv2.ellipse( img, el, 255 )
        # Get the values from these ares
        sig = get_signal( img, el )
        data_[ el ].append( (nframes_, sig ) )

    cv2.imshow( "main", img )
    cv2.waitKey( waitFor )



def custom_draw( kp1, kp2, good, frame ):
    return frame
    for p in kp2:
        pt = int( p.pt[0] ), int( p.pt[1] )
        cv2.circle( frame, pt, 3, 255, -1 )
    return frame

def resize( frame, fx=0.5, fy=0.5 ):
    frame = cv2.resize(frame, None, fx=fx, fy=fy, interpolation = cv2.INTER_LINEAR)
    return frame

def find_bee( template, frame ):
    global nframes_ 
    print( 'Processing frame %d' % nframes_ )
    tw, th = template.shape
    fw, fh = frame.shape
    nc, nr = int(fw/tw)-1, int(fh/th)-1
    for i in range( nc ):
        for j in range( nr ):
            rect = frame[i*tw:(i+1)*tw,j*th:(j+1)*th]
            good = [ ]
            try:
                good, k = hb.detectTemplate( template, rect )
            except Exception as e:
                pass
            if len( good ) > 10:
                frame[i*tw:(i+1)*tw,j*th:(j+1)*th] = 255

    show_image( )
    return 

    good, (kp1, kp2) = hb.detectTemplate( template, frame )
    newF = np.zeros_like( frame )
    if len(good) > 10:
        print( 'x', end='')
        sys.stdout.flush( )
        newF = custom_draw( kp1, kp2, good, frame )
        #newF = cv2.drawMatches( template, kp1, frame, kp2, good, newF
        #        , singlePointColor = 255 
        #        #, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        #        )
        show_image( newF, waitFor = 1 )
    else:
        print( '.', end='' )
        sys.stdout.flush( )

def process( orig, fgbg = None ):
    global args_
    global frames_, nframes_
    global avg_
    print( 'Processing frame %d' % nframes_ )
    frame = cv2.blur( orig, (5,5) )
    mu, sigma = np.mean( frame ), np.std( frame )
    #frame[ frame >= args_.threshold ] = 255
    if fgbg is not None:
        frame = fgbg.apply(frame)

    avg_ = ( nframes_ * avg_ + frame ) / (nframes_ + 1.0 )
    # show_image( np.uint8(255.0 * avg_ / avg_.max( )), orig, 1 )
    show_image( orig, waitFor = 1 )

def main( args ):
    global args_
    global nframes_
    global avg_

    args_ = args
    cap = cv2.VideoCapture( args_.video )
    template = cv2.imread( "./template_honeybee.png", 0 )

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_ = resize( gray )
    fgbg = cv2.createBackgroundSubtractorKNN()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = resize( cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) )
        current_frame_ = gray
        process( gray )
        nframes_ += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    outfile = '%s.pickle' % (args_.video )
    with open( outfile, 'wb') as f:
        pickle.dump( data_, f )
    print( 'Saved analysis data to %s' % outfile )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Analyze Bee video'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--video', '-v'
        , required = True
        , help = 'Input video file'
        )
    parser.add_argument('--threshold', '-t'
        , required = True, type = float
        , default = 50
        , help = 'Threshold'
        )
    parser.add_argument( '--debug', '-d'
        , required = False
        , default = 0
        , type = int
        , help = 'Enable debug mode. Default 0, debug level'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
