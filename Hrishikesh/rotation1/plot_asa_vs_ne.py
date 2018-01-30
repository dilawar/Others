#!/usr/bin/env python

"""plot_asa_vs_ne.py: 

Plot ASA vs Normalized Energy. Ask Hrishikesh if you are confused.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import pickle
import pandas as pd
from collections import defaultdict
import glob

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use( 'bmh' )
mpl.rcParams['axes.linewidth'] = 0.2
mpl.rcParams['lines.linewidth'] = 1.0
mpl.rcParams['text.usetex'] = False

if not os.path.isdir( '_images' ):
    os.makedirs( '_images' )


def process( f, d, data ):
    global xvec
    global yvec
    print( '[INFO] Processing %s' % f )
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    id_ = os.path.basename( f )[:4]
    nrForId = data.get( id_, None )
    if nrForId is None:
        print( '[WARN] No data is found for %s' % id_ )
        return
    ne = d[ 'avg' ].values
    cols = alpha[:len(d)]
    scatter = defaultdict( list )

    xvec, yvec = [ ], [ ]
    for i, c in enumerate(cols):
        for k in nrForId:
            frm, to = k.split( '-' )
            if c == frm:
                scatter[c].append( nrForId[k] )
                xvec.append( ne[i] )
                yvec.append( float(nrForId[k]) )
    return id_, xvec, yvec


def main( ):
    data = None
    with open( sys.argv[1], 'rb' ) as f:
        data = pickle.load( f )

    files = glob.glob( './toplot/*' )
    plt.figure( )
    for f in files:
        d = pd.read_csv( f, sep = '\t' )
        if len( d ) < 1:
            continue
        res = process(f, d, data )
        if res is not None:
            l, x, y = res
            plt.plot( x, y, 'o', label = l )
            #plt.legend(loc='best', framealpha=0.4)

    plt.xlabel( 'PSA' )
    plt.ylabel( r'NE/Residue' )

    outfile = '%s.png' % sys.argv[1] 
    plt.tight_layout( )
    plt.show( )
    plt.savefig( outfile )
    print( 'Plot saved to %s' % outfile )
    print( 'All done' )
    



if __name__ == '__main__':
    main()
