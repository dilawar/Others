#!/usr/bin/env python
"""main.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from oiffile import OifFile
import cv2

def stats( image ):
    m, mx = np.min( image ), np.max( image )
    mean, std = np.mean( image ), image.std( )
    return m, mx, mean, std 

def equalize( image, cuttoff = 0.9 ):
    ys, bins = np.histogram( image, bins = 100 )
    allVals = np.sum( ys )
    runningSum = 0.0
    cuttOffBin = 0
    for y, b in zip( ys, bins ):
        runningSum += y
        if runningSum >= cuttoff * allVals:
            cuttOffBin = int( b )
            break
    image[ image < cuttOffBin ] = 0.0
    return image

def find_cell( y0, x0, image, newImg, thres = 0 ):
    val = image[x0, y0]
    cell = [ (y0,x0) ]
    pivots = [(y0, x0)]
    while pivots:
        y0, x0 = pivots.pop( 0 )
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                y, x = y0 + dy, x0 + dx 
                try:
                    if image[x, y] > (val ** 0.5):
                        image[x, y] = 0
                        newImg[x, y] = val
                        cell.append( (y,x) )
                        pivots.append( (y,x) )
                except IndexError as e:
                    pass
    return cell

def find_cells( image, green, blue ):
    thresStop = 1
    minMax = cv2.minMaxLoc( image )
    cells = [ ]
    cellFile = '%s.csv' % sys.argv[1]
    with open( cellFile, 'w' ) as f:
        f.write( 'y,x,size,blue,green,ratio\n' )

    bbyg = [ ]
    newImg = np.zeros( image.shape )
    while minMax[1] > thresStop:
        y, x = minMax[-1]
        val = image[ x, y ]
        cell = find_cell( y, x, image, newImg ) 
        minMax = cv2.minMaxLoc( image )
        if len( cell ) >= 5:
            cells.append( cell )
            with open( cellFile, 'a' ) as f:
                b = np.mean( [ blue[x,y] for y, x in cell ] )
                g = np.mean( [ green[x,y] for y, x in cell ] )
                bbyg.append( b / g )
                f.write( "%d,%d,%d,%g,%g,%g\n" % (y, x, len(cell), b, g, b/g))
    return cells, newImg, bbyg

def process( filename ):
    with OifFile( filename ) as f:
        data = f.asarray( )

    blue, green = data[0,:,:], data[1,:,:]
    image = np.copy( green )
    image = equalize( image )
    cells, newImg, bbyg = find_cells( image, green, blue )
    print( '[INFO] Total cells %d' % len( cells ) )
    print( '[INFO] Plotting ' )

    plt.subplot( 221 )
    plt.imshow( blue )
    plt.title( 'Blue' )
    plt.subplot( 222 )
    plt.imshow( green )
    plt.title( 'Green' )
    plt.subplot( 223 )
    plt.imshow( newImg )
    plt.title( 'Identified Cells' )

    plt.subplot( 224 )
    plt.hist( bbyg, bins = 30 ) 
    plt.savefig( '%s.png' % sys.argv[1] )

def main( ):
    imagingFile = sys.argv[1]
    process( imagingFile )

if __name__ == '__main__':
    main()
