"""
Locate mouse by template tracking.

"""
    
__author__           = "Me"
__copyright__        = "Copyright 2016, Me"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Me"
__email__            = ""
__status__           = "Development"

import cv2
import math
import numpy as np

trajectory_ = [ ]
curr_loc_ = None

def onmouse(event, x, y, flags, params):
    global current_frame_, bbox_
    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox_ = []
        bbox_.append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        bbox_.append((x, y))
        cv2.rectangle(current_frame_, bbox_[0], (x,y), 0,2)

def toGrey( frame ):
    return cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )

def display_frame( frame, delay = 40 ):
    try:
        cv2.imshow( 'frame', frame )
        cv2.waitKey( delay )
    except Exception as e:
        print( '[warn] could not display frame' )
        print( '\t Error was %s' % e )

def clip_frame( frame, box ):
    (r1, c1), (r2, c2 ) = box
    return frame[c1:c2,r1:r2]

def generate_box( (c,r), width, height ):
    if width < 0: width = 10
    if height < 0 : height = 10
    leftCorner = ( max(0,c - width / 2), max(0, r - height / 2 ) )
    rightCorner = (leftCorner[0] + width, leftCorner[1] + height)
    return leftCorner, rightCorner 

def apply_template( frame, tmp ):
    tr, tc = tmp.shape    # Rows and cols in template.
    res = cv2.matchTemplate( frame, tmp, cv2.TM_SQDIFF_NORMED )
    minmax = cv2.minMaxLoc( res )
    minv, maxv, minl, maxl = minmax
    return minl

def is_far_from_last_good_location( loc ):
    global lastGoodLocation_ 
    if lastGoodLocation_ is None:
        return False
    x1, y1 = lastGoodLocation_ 
    x2, y2 = loc 
    dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 
    if dist < 5.0:
        return True
    return False


def track_using_templates( frame ):
    global lastGoodTemplate_
    global lastGoodLocation_ 

    # if last good location of mice is not known, then we apply the first
    # template and get it.
    if lastGoodTemplate_ is not None:
        indx = lastGoodTemplate_[0]
        ranges = np.mod( 
                np.arange( indx, indx + len( templates_ ), 1 )
                , len( templates_ ) 
                )
    else:
        ranges = np.arange( 0, len( templates_ ) )

    for i in ranges:
        tmp = templates_[i]
        tr, tc = tmp.shape    # Rows and cols in template.
        loc = apply_template( frame, tmp )
        if is_far_from_last_good_location( loc ):
            continue 
        else:
            lastGoodLocation_ = loc
            lastGoodTemplate_ = (i, tmp)
            break
    r, c = lastGoodLocation_
    print( "Last known good location is %s" % str( lastGoodLocation_ ) )
    return frame[c-100:c+100,r-100:r+100]


def is_a_good_frame( frame ):
    if frame.max( ) < 100 or frame.min() > 150:
        print( '[WARN] not a good frame: too bright or dark' )
        return False
    if frame.mean( ) < 50 or frame.mean() > 200:
        print( '[WARN] not a good frame: not much variation' )
        return False
    return True

def fetch_a_good_frame( drop = 0 ):
    global cap_
    for i in range( drop ):
        ret, frame = cap_.read()
    ret, frame = cap_.read()
    if ret:
        if is_a_good_frame( frame ):
            return frame
        else:
            return fetch_a_good_frame( )
    else:
        print( '[Warn] Failed to fetch a frame' )
        return None

def track_using_trajectories( cur, prev ):
    global curr_loc_ 
    p0 = cv2.goodFeaturesToTrack( prev, 100, 0.1, 30 )
    p1, status, err = cv2.calcOpticalFlowPyrLK( prev, cur, p0 )
    mat = cv2.estimateRigidTransform( p0, p1, False )
    # print cv2.warpAffine( curr_loc_, mat, dsize=(2,1) )
    if mat is not None:
        dx, dy = mat[:,2]
        da = math.atan2( mat[1,0], mat[0,0] )
        trajectory_.append( (dx, dy, da) )
        print( "Transformation", dx, dy, da )
        curr_loc_ = (curr_loc_[0] - int(dy), curr_loc_[1] - int(dx))

def process( args ):
    global cap_
    global box_, templates_
    global curr_loc_ 
    curr_loc_ =  np.array( [ args.col, args.row ], dtype = np.uint8 )
    cap_ = cv2.VideoCapture( args.file )
    nFames = cap_.get( cv2.cv.CV_CAP_PROP_FRAME_COUNT )
    fps = float( cap_.get( cv2.cv.CV_CAP_PROP_FPS ) )
    print( '[INFO] FPS = %f' % fps )
    cur = fetch_a_good_frame( )
    cur = toGrey( cur )
    while True:
        totalFramesDone = cap_.get( cv2.cv.CV_CAP_PROP_POS_FRAMES ) 
        if totalFramesDone + 1 >= nFames:
            print( '== All done' )
            break
        prev = cur.copy()
        cur = fetch_a_good_frame( drop = 5 )
        cur = toGrey( cur )
        track_using_trajectories( cur, prev )
        cv2.circle( cur, curr_loc_, 20, 255, 2 )
        cv2.imshow( 'Frame', cur )
        cv2.waitKey( 1 )

def main(args):
    # Extract video first
    process( args )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Detect eye blinks in given recording.'''
    parser = argparse.ArgumentParser(description=description)
    class Args: pass 
    args = Args()
    parser.add_argument('--file', '-f'
        , required = False
        , default = 0
        , help = 'Path of the video file or camera index. default camera 0'
        )
    parser.add_argument('--bbox', '-b'
        , required = False
        , nargs = '+'
        , type = int
        , help = 'Bounding box : topx topy width height'
        )
    parser.add_argument('--verbose', '-v'
        , required = False
        , action = 'store_true'
        , default = False
        , help = 'Show you whats going on?'
        )
    parser.add_argument('--template', '-t'
        , required = False
        , default = None
        , type = str
        , help = 'Template file'
        )

    parser.add_argument('--col', '-c'
            , required = True , type = int , help = 'Column of mouse'
            )
    parser.add_argument('--row', '-r'
            , required = True , type = int, help = 'Row index of mouse'
            )
    parser.parse_args(namespace=args)
    main( args )

