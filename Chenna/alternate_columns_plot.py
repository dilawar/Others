"""alternate_columns_plot.py: 


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
import pandas
# plt.style.use( 'ggplot' )

def main():
    """docstring for main"""
    data = pandas.read_csv( sys.argv[1], sep = ',' )
    data = data.fillna( 0 )
    xcols, ycols =  [], []
    for i, c in enumerate(data.columns):
        if i % 2 == 0:
            xcols.append( c )
        else:
            ycols.append( c )

    plt.subplot( 211 )
    img =  [ ]
    for x, y in zip( xcols, ycols ):
        xdata = data[ x ].values
        ydata = data[ y ].values
        plt.plot( xdata / 1e6, ydata, label = '%s vs %s' % (x, y) )
        img.append( ydata )

    plt.ylabel( 'sRNA abundance' )
    plt.xlabel( 'Chromosome coordinates (Mb)' )

    plt.subplot( 212 )
    plt.imshow( np.vstack( img ), interpolation = None, aspect = 'auto' )
    plt.colorbar( )


    outfile = '%s.png' % sys.argv[1]
    plt.tight_layout( )
    plt.savefig( outfile )
    print( 'Saved to %s' % outfile )
    

if __name__ == '__main__':
    main()

