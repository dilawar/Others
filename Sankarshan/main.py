"""main.py: 

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
import matplotlib.pyplot as plt
import numpy as np
import reader
from config import _logger

def main( ):
    channelDict = reader.collect_data( sys.argv[1] )
    channels = channelDict.keys( )
    firstFrames = [ channelDict[ch][0] for ch in channels ]

    # First test is on the sum of frames. 
    plt.figure( )
    for i, ch in enumerate( channels ):
        # plt.subplot( len( channels ), 1, i + 1 )
        yvec = [ np.sum(x[1]) for x in channelDict[ ch ] ]
        plt.plot( yvec, label = ch )
        plt.legend(loc='best', framealpha=0.4)

    plt.savefig( 'test1.png' )



if __name__ == '__main__':
    main()
