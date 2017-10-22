"""detect_species.py: 

    Given a template in PNG and library files in tiff, detect the template.

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
import glob
from libtiff import TIFF
import cv2
import numpy as np

FLANN_INDEX_KDTREE = 0
MIN_MATCH_COUNT = 10

kpTemp_, desTemp_ = None, None
debug_ = False
templdir = "."
resdir = "_result"
current_f_index_ = 0

if not os.path.isdir( resdir ):
    os.makedirs( resdir )

def show_frame( frame, block = False ):
    cv2.imshow( 'Frame', frame )
    if not block:
        cv2.waitKey( 1 )
    else:
        cv2.waitKey( -1 )

def find_all_files( library ):
    tiffs = [ ]
    for d, sd, fs in os.walk( library ):
        for f in fs:
            ext = f.split( '.' )[-1]
            if ext in [ 'tiff', 'TIFF', 'tif', 'TIF' ]:
                tiffs.append( os.path.join( d, f ) )
    print( 'Found %d tiff files in library' % len( tiffs ) )
    return tiffs


def detectTemplate( template, frame):
    global kpTemp_, desTemp_ 
    global templdir
    global current_f_index_ 
    sift = cv2.xfeatures2d.SIFT_create( sigma = 1.2, nOctaveLayers = 5 )
    kpTemp_, desTemp_ = sift.detectAndCompute( template, None )
    assert desTemp_ is not None
    return searchForTemplate( sift, template, frame )

def searchForTemplate( sift, template, f ):
    global kpTemp_, desTemp_
    global templdir
    global current_f_index_

    #f = cv2.bilateralFilter( f, 13, 5, 7 )
    kp, des = sift.detectAndCompute( f, None )
    bf = cv2.BFMatcher( )
    matches = bf.knnMatch(desTemp_, des, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 1.0 * n.distance:
            good.append(m)

    return good, (kpTemp_, kp)


def main( ):
    templateFile = sys.argv[1]
    imgfile = sys.argv[2]
    detectTemplate( templateFile, imgfile )

if __name__ == '__main__':
    main()
