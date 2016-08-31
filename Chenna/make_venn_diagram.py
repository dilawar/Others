"""make_venn_diagram.py: 

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
from collections import defaultdict
import sys
from matplotlib_venn import venn3, venn3_circles

def key_to_decimal( key ):
    val, i = 0, 0
    for v in reversed(key):
        val += v * (10 ** i )
        i += 1
    return val

def process( files ):
    data = []
    print( '[INFO] Processing %s' % files )
    for filename in files:
        with open( filename, 'r' ) as f:
            lines = f.read().split('\n')
            lines = filter(None, lines)
            fields = [ x.split() for x in lines[1:] ]
            data.append( [ f[2] for f in fields] )

    allGenes = []
    for gene in data:
        allGenes += gene
    allGenes = set(allGenes)
    print( '[INFO] Total unique genes = %d' % len( allGenes ) )

    venns = defaultdict( list )

    # Initialized the keys.
    for k in [ 1, 2, 3, 12, 13, 23, 123 ]:
        venns[k] = []

    for g in allGenes:
        key = []
        for i, d in enumerate(data):
            if g in d:
                key.append(i+1)
        kd = key_to_decimal( key )
        venns[kd].append(g)

    for k in venns:
        print k
        print venns[k]
        print "======"

    count = []
    for k in venns:
        count.append( len(venns[k]) )

    venn3( count, set_labels = files )
    plt.savefig( 'output.png' )
    print( '[INFO] Saved to output.png' )
    plt.close()


def main():
    files = sys.argv[1:]
    process( files )


if __name__ == '__main__':
    main()
