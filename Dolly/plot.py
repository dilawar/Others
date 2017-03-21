"""plot.py: 

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
import math
import matplotlib.cm as cm
import numpy as np
import random
import pandas
from collections import defaultdict, OrderedDict

import matplotlib as mpl
import matplotlib.pyplot as plt
print( plt.style.available )
plt.style.use( 'seaborn-deep' )

mpl.rcParams.update( { 'font.size' : 28 } )

random.seed( 0 )

families_ = OrderedDict( )
targets_  = [ ]
colors_ = OrderedDict( )

def sortFamily( keys ):
    print( keys )
    keys[8], keys[10] = keys[10], keys[8]
    return keys

def plotthis( data ):
    global families_, targets_
    data = data.sort_values( by='type' )
    families = data[ 'Species' ].drop_duplicates( )
    for i, family in enumerate( families ):
        items = data[ data['Species'] == family ]
        families_[ family ] = items
        [ targets_.append( x ) for x in list(items[ 'Annotation' ] ) ]
    targets_ = list( set(targets_) )

    # start plotting
    fig = plt.figure( figsize=(50, 50) )
    pad_ = 0.25
    ax = fig.add_axes( [0.35, 0.3, 0.5, 0.5 ], polar = True )
    ax.grid( False )
    # ax.axis( 'off' )

    theta = 0.0
    spacing = 3
    totalSpokes = len( set(data['Strain'] ) )
    #print(( 'total spokes %d' % totalSpokes ))
    stepTheta = 2 * np.pi /  ( totalSpokes + spacing * len( families_) )

    bottom_ = 100
    spokeLen = 10
    # maxW = len( targets_ ) * spokeLen + bottom
    # maxW = 150
    thetaGridPos, thetaGridLabels = [ ], [ ]
    groupPos, groupLabel = [], []
    legends = [ ]
    cmap = cm.get_cmap( 'Paired_r', lut = 36 )
    # for family in sorted( families_, reverse = True ):
    typeZeroEndsAngel = 0

    familitySorted = sortFamily( families_.keys( ) )

    for family in familitySorted:
        groupLabel.append( family )
        groupPos.append( theta )

        group = families_[ family ]
        groupSize = len( group )
	#print(( 'Goup %s size %d' % ( family, groupSize ) ))
        # print( '\t%s' % rnas )
        allTargets = list( set( group[ 'Annotation' ] ) )

        groups = list( set( group[ 'Strain' ] ) )
        # print( groups )

        for gi, item in enumerate( groups ):
            targets = set( group[ group['Strain'] == item ]['Annotation'].values )
            theta += stepTheta
            for i, t in enumerate(targets):
                # This is most likely to an NaN
                # print( '+ %s is targets' % t )
                label_ = '_nolegend_'
                if t not in legends:
                    try:
                        label_ = str(t).decode('utf-8')
                    except Exception as e:
                        label_ = '%s' % t
                    legends.append( t )
                    colors_[ t ] =  len( colors_ )

                clr = cmap( colors_[t] )
                # x = len( legends ) / 40.0
                # clr = ( x, 0, x )
                if t != 'NONE':
                    bar = ax.bar( theta
                            , spokeLen
                            , 0.5*stepTheta
                            # , bottom = bottom_ + allTargets.index( t ) * spokeLen 
                            , bottom = bottom_ + i * spokeLen 
                            , color = clr , edgecolor = clr
                            , label = label_
                            )

                proteinBar = ax.bar( theta
                        , 4 * getAntarProteinMean( item, data )
                        , 0.3 * stepTheta
                        , bottom = 50
                        , color = 'black'
                        )
                ax.set_yticks( 
                        [ 8*theta,9*theta,10*theta,11*theta, 12*theta, 13*theta
                            , 14*theta, 15*theta, 16*theta ]
                        , minor=True
                        )
                ax.yaxis.grid(True, which='major')
                ax.yaxis.grid(True, which='minor')


            thetaGridPos.append( 180 /  np.pi * theta )
            label = item
            thetaGridLabels.append( label )

        theta += spacing * stepTheta
        # Compute the boundry of all family of type 0
        _type = data[ data['Species'] == family ]['type'].values[0]
        if _type == 0:
            typeZeroEndsAngel = theta

    # Draw a background slice for all type = 0.
    ax.bar( 0, 100, typeZeroEndsAngel, color = 'blue', bottom = 50 
            , alpha = 0.1
            )

    # Set family names
    ax.set_yticks( [] , [] )
    set_label( ax, thetaGridPos, thetaGridLabels )
    #maxW = 150
    #for x, p in zip( groupPos, groupLabel ):
    #	l = ax.annotate( p, xy = (x-20, maxW-30), xytext = (x, maxW+25) )
     #   ang = 180 * x / np.pi 
      #  l.set_rotation( ang - 90 )
       # l.set_ha( 'center' )
        #l.set_va( 'top' )
        # if ang > 90 and ang < 180:
            # l.set_va( 'bottom' )
        # if ang < 180:
            # l.set_va( 'bottom' )
        # elif ang > 180:
            # l.set_va( 'top' )
        # print x, p
    print( 'Saved to result.png' )
    plt.legend( loc = 2, framealpha = 0.0
            , bbox_to_anchor = (-0.7, 0.45 )
            )
    # plt.savefig( 'result.eps', format='eps', dpi=900 )
    plt.savefig( 'result.png' )

def getAntarProteinMean( s, data ):
    antarP = data[ data['Strain'] == s ]['Number of ANTAR proteins'].mean( )
    return antarP 

def set_label( ax, pos, labels, frac = 1.1 ):
    lines, labels = ax.set_thetagrids( pos, labels = labels, frac = frac )
    for i, l in enumerate( labels ):
        ang = float(  pos[ i ] )
        l.set_rotation( ang )
        l.set_ha( 'left' )
        if ang > 90 and ang < 270:
            l.set_ha( 'right' )
        if ang < 180:
            l.set_va( 'bottom' )
        elif ang > 180:
            l.set_va( 'top' )
        
def main():
    """docstring for main"""
    data = pandas.read_table( sys.argv[1], sep = '\t' )
    plotthis( data )
    

if __name__ == '__main__':
    main()
