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
mpl.style.use( 'bmh' )
mpl.rcParams['axes.linewidth'] = 0.2
mpl.rcParams['lines.linewidth'] = 1.0


def plot( df ):
    df = df[ df['Bouts'] <= 16 ]

    startT = datetime.datetime.strptime( '8:00', '%H:%M' )

    res = pd.DataFrame( )
    t0s, t1s, turnovers = [], [], []
    for i in range( 24 ):
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
    res.to_csv( '%s_turnover.csv' % sys.argv[1] )

    xvec, yvec = list(range(len(turnovers))), turnovers

    newX = np.linspace( min(xvec), max(xvec), 100 )
    smoothY = sinp.spline( xvec, yvec, newX )

    # plot.
    plt.plot( xvec, yvec, '-o', lw=2, label = 'Turnover' )
    #plt.plot( newX, smoothY, lw = 2 )
    plt.ylabel( 'Turnover' )
    plt.savefig( '%s.png' % sys.argv[1] )
    print( 'All done' )



def main( ):
    df = pd.read_csv( sys.argv[1], sep = ',' )
    df['timestamp' ] = pd.to_datetime( df[ 'Time' ], format='%H:%M' ).dt.time
    plot( df )

if __name__ == '__main__':
    main()
