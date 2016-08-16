"""gaps_detection.py: 

Detecting gaps in recordings.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import cv2

def process( filename ):
    print( 'Processing %s' % filename )
    cap = cv2.VideoCapture( filename )

def main( ):
    filename = sys.argv[1]
    process( filename )

if __name__ == '__main__':
    main()
