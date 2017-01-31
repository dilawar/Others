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
import itertools
from config import _logger

def main( ):
    dataDir = sys.argv[1]
    channelDict = reader.collect_data( dataDir )
    channels = channelDict.keys( )
    firstFrames = [ channelDict[ch][0] for ch in channels ]

    # First test is on the sum of frames. 
    plt.figure( )
    plt.subplot( 211 )

    scatter = [ ]
    for i, ch in enumerate( channels ):
        # plt.subplot( len( channels ), 1, i + 1 )
        yvec = [ np.mean(x[1]) for x in channelDict[ ch ] ]
        yerr = [ np.std(x[1]) for x in channelDict[ ch ] ]
        scatter.append( yvec )
        plt.errorbar( range( len(yvec) ), yvec, yerr = yerr, label = ch )
        plt.legend( framealpha=0.4)

    plt.subplot( 212 )
    for x, y in itertools.combinations( scatter, 2 ):
        m, c = np.polyfit(x, y, 1)
        plt.scatter( x, y, label = '%f x + %f' % (m, c) )
        lineFunc = lambda k : k * m + c
        plt.plot( x, [ lineFunc( xx ) for xx in x ] )
        plt.legend( framealpha=0.4)

    plt.tight_layout( )
    plt.savefig( os.path.join( dataDir, 'mean_stdvar_of_each_frame.png' ) )

    # Test 2. Do the same analysis pixel by pixel.
    m, n = firstFrames[0][1].shape
    imgs = [ np.zeros( shape = (m,n) ) for ch in channels ]
    plt.figure( )

    comparisons = list(itertools.combinations( channels, 2 ))
    for nc, (ch1, ch2) in enumerate( comparisons ):
        # plot m and c heat map.
        ch1Data = [ x[1] for x in channelDict[ ch1 ] ]
        ch2Data = [ x[1] for x in channelDict[ ch2 ] ]
        mImg = np.zeros( shape=(m,n) )
        cImg = np.zeros( shape=(m,n) )
        for i, j in itertools.product( range( m ), range( n ) ):
            _logger.debug( 'Computing for pixel %d and %d' % (i, j) )
            ch1Y = [ frame[i, j] for frame in ch1Data ]
            ch2Y = [ frame[i, j] for frame in ch2Data ]
            m, c = np.polyfit( ch1Y, ch2Y, 1 )
            mImg[i, j ] = m
            cImg[ i, j ] = c

        plt.subplot( len(comparisons), 2, nc + 1 )
        plt.imshow( mImg, aspect = 'auto', interpolation = 'none' )
        plt.colorbar( )
        plt.title( 'slope of fit' )
        # plt.legend( framealpha=0.4)
        plt.subplot( len(comparisons), 2, nc + 2 )
        plt.imshow( cImg, aspect = 'auto', interpolation = 'none' )
        plt.colorbar( )
        plt.title( 'Intercept of fit' )
        
    plt.tight_layout( )
    outfile = os.path.join( dataDir, 'pixel_comparison_linear.png' )
    plt.savefig( outfile )
    _logger.info( 'Saved to %s' % outfile )



if __name__ == '__main__':
    main()
