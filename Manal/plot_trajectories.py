#!/usr/bin/env python

"""plot_trajectories.py: 

    Plot given trajectories.

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
from matplotlib.collections import LineCollection
import numpy as np
import scipy
import matplotlib
import scipy.io

matplotlib.rc( 'text', usetex= True )

try:
    plt.style.use( 'ggplot' )
except Exception as e:
    pass

def calc_velocity( xs, ys, ts ):
    ts = np.ravel( ts )
    xs = np.ravel( xs )
    ys = np.ravel( ys )
    dts = np.diff( ts, axis = 0)
    vel = np.zeros( len(xs) )
    for i, x in enumerate( xs ):
        try:
            dist = ((xs[i+1] - xs[i]) ** 2  + (ys[i+1] - ys[i]) ** 2) ** 0.5
            vel[i] = dist / dts[i]
        except Exception as e:
            #print( '[WARN] More timepoints than positions' )
            pass
    return vel

def plot( xpos, ypos, velocity, angle, plot_type = 'simple' ):
    fig = plt.figure( )

    if plot_type == 'quiver':
        raise UserWarning( 'Not implemented : quiver' )
        return

    traA = plt.subplot2grid( (2,3), (0,0), rowspan = 2, colspan = 2, aspect = 1 )
    velA = plt.subplot2grid( (2,3), (0,2), colspan = 1 )
    angA = plt.subplot2grid( (2,3), (1,2), colspan = 1 )
    startN = 1
    p = traA.scatter( xpos[startN:], ypos[startN:], c = velocity[startN:], marker = '.', lw=0 )

    # start position
    start = (xpos[0], ypos[0] )
    # textStart = ( xpos[0] - 100, ypos[0] - 100 )
    textStart = ( 500, 500 )
    traA.annotate( 'start', xy = start, xytext = textStart
            , arrowprops = dict( facecolor = 'black', shrink = 0.1 
                , width = 2
                )
            )

    traA.set_title( 'Trajectory' )
    traA.set_xlabel( 'x position' )
    traA.set_ylabel( 'y position' )
    traA.set_xlim( [ 0, 1000 ] )
    traA.set_ylim( [ 0, 1000 ] )

    circle = matplotlib.patches.Circle(
            xy = (500,500), radius = 500
            , edgecolor = "k", facecolor = "none"
            )
    plt.colorbar( p , ax = traA, orientation = 'horizontal' )
    traA.add_patch(circle)

    # make the axis invisible 
    # traA.axis( 'off' )
    # for loc, spine in traA.spines.iteritems():
        # use ax.spines.items() in Python 3
        # spine.set_linewidth(0)

    # X, Y = np.meshgrid( range( len(xpos)), range( len(ypos) ) )
    # plt.quiver( X, Y, xpos, ypos, angle )
    velA.hist( velocity, bins = 20 )
    velA.set_title( 'Velocity' )
    angA.hist( angle, bins = 20 )
    angA.set_title( 'Head orientation angle' )
    plt.tight_layout( )

def main( args ):
    print( '[INFO] Reading file %s' % args.filepath )
    data = scipy.io.loadmat( args.filepath )
    # for k in data.keys():
        # print("[INFO] \t %s, %s" % (k, data[k]) )
    xpos, ypos = data['x_pos'], data['y_pos']
    angle = np.ravel( data['angle'] )
    timestamps = data['timestamps']
    velocity = calc_velocity( xpos, ypos, timestamps )
    plot( xpos, ypos, velocity, angle )
    outfile = args.outfile or '%s_out.png' % args.filepath   
    plt.savefig( outfile )
    print( '[INFO] Wrote output file to %s' % outfile )
    plt.close( )



if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Plot trajectories'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--filepath', '-f'
        , required = True
        , help = 'Input file'
        )
    parser.add_argument('--outfile', '-o'
        , required = False
        , help = 'Plotted trajectory saved to this file'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
