"""reader.py: 

Reads tiff file in given directory, recursively.

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
import os
import tifffile
import re
from collections import defaultdict
import tifffile

def collect_data( dirname ):
    tiffs = defaultdict( list )
    pat = re.compile( r'img_(?P<id>\d+)_(?P<channel>.+?)\.tif', re.I )
    for d, sd, fs in os.walk( dirname ):
        for f in fs:
            if f.split( '.' )[-1].lower( ) in [ 'tif', 'tiff' ]:
                m = pat.search( f )
                if m:
                    imgId, imgChannel = m.group( 'id' ), m.group( 'channel' )
                    # tiffs imgId ][ imgChannel ] = tifffile.imread(os.path.join( d, f )) 
                    tiffs[ imgChannel ].append( 
                            (f, tifffile.imread(os.path.join( d, f )))
                            )

    return tiffs
