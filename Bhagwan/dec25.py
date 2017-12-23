"""dec25.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import numpy as np
import scipy.interpolate as sinp
import pandas as pd
import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    mpl.style.use( 'seaborn-poster' )
except Exception as e:
    print( e )
    pass

tempdir = '_temp'
if not os.path.exists( tempdir ):
    os.makedirs( tempdir )

def timeToStr( t ):
    return '%02d:%02d' % ( t.hour, t.minute )

def process( filepath, plot = True  ):
    filename = os.path.basename( filepath )

    imgpath = os.path.join( tempdir, '%s.png' % filename )
    respath = os.path.join( tempdir, '%s.csv' % filename )

    print( 'Processing %s' % filepath )
    df = pd.read_csv( filepath, sep = ',' )
    df['timestamp' ] = pd.to_datetime( df[ 'Time' ], format='%H:%M' ).dt.time
    df = df[ df['Bouts'] <= 16 ]

    startT = datetime.datetime.strptime( '8:00', '%H:%M' )
    res = pd.DataFrame( )
    t0s, t1s, turnovers = [], [], []
    for i in range( 21 ):
        dt = datetime.timedelta( minutes = 30 )
        t0 = (startT + i * dt).time()
        t1 = (startT + (i+1) * dt).time()
        entries = df[ df[ 'timestamp' ] >= t0 ]
        entries = entries[ entries['timestamp'] <= t1 ]
        t0s.append( t0 )
        t1s.append( t1 )
        turnovers.append( len(entries[ 'Bouts' ].values ) )

    res[ 't_start' ] = t0s
    res[ 't_end' ] = t1s
    res[ 'turnover' ] = turnovers
    res.to_csv( respath )

    if plot:
        plt.figure( )
        xvec, yvec = list(range(len(turnovers))), turnovers
        newX = np.linspace( min(xvec), max(xvec), 100 )
        smoothY = sinp.spline( xvec, yvec, newX )
        plt.bar( xvec, yvec )
        plt.xticks( xvec[::2], [ timeToStr( x) for x in t0s[::2] ], rotation = 'vertical' )
        plt.ylabel( 'Turnover' )
        plt.xlabel( 'Bin Size = 30 min' )
        plt.tight_layout( )
        plt.savefig( imgpath )
        plt.close( )
        print( 'All done' )

    return res

def main( ):
    files = [ ]
    for d, ds, fs in os.walk( sys.argv[1] ):
        for f in fs:
            if '.csv' in f:
                files.append( os.path.join( d, f ) )

    results = [ process( f ) for f in files ]
    img = [ ]
    plt.subplot( 211 )
    for i, res in enumerate( results ):
        t0s = res[ 't_start' ]
        yvec = res[ 'turnover' ]
        xvec = np.arange( 0, len(yvec) )
        img.append( yvec )
        plt.bar( xvec + i * 0.1, res[ 'turnover' ], width=0.05, alpha = 0.8)

    plt.xticks( xvec[::2], [ timeToStr( x) for x in t0s[::2] ], rotation = 'vertical' )

    img = np.array( img )
    yerr = np.std( img, axis = 0 )
    mean = np.mean( img, axis=0)
    plt.subplot( 212 )
    plt.plot( xvec, mean, lw = 5, color = 'blue' )
    plt.fill_between( xvec, mean + yerr, mean - yerr, alpha = 0.5 )
    plt.xticks( xvec[::2], [ timeToStr( x) for x in t0s[::2] ], rotation = 'vertical' )
    plt.xlabel( 'Time Bin = 30 m' )
    plt.suptitle( 'Turnover', fontsize = 20 )
    plt.tight_layout( rect = (0,0,1,0.9) )
    plt.savefig( 'results.png' )

if __name__ == '__main__':
    main()
