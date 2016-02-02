#!/usr/bin/env python 

"""turns_in_swim.py: 

Angle and amplitude of turn in Zebrafish swim data.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"


import numpy as np
import scipy.signal as signal
import pylab


args_ = None

def get_width(i, vec):
    width = 0
    r = i
    while vec[r] > 0:
        r += 1
    l = i-1
    while vec[l] > 0:
        l -= 1
    return  (r - l)

def get_turns( yvec ):
    global args_
    turns = []
    pylab.subplot(2, 1, 2)
    width = 20
    vec = np.convolve( yvec, np.ones( width ) /width  , 'same' )
    peakIds = signal.find_peaks_cwt( vec, np.arange(args_.min_width, 50) )
    amplitudes = [ vec[i] for i in peakIds ]
    widths = [ get_width( i, vec ) for i in peakIds ]
    pylab.plot( vec, label = 'Filtered window=%d' % width )
    pylab.legend(loc='best', framealpha=0.4)
    pylab.plot( peakIds, amplitudes, 'o' )
    for i, x in enumerate(peakIds):
        turns.append( (x, amplitudes[i], widths[i] ) )
    return turns

def accept_turn( turn, mean ):
    loc, amp, width = turn
    if amp <= 0.0:
        print('[REJECTED] Turn at index %s' % loc)
        return False
    return True


def main( args ):
    global args_
    args_ = args
    data = np.genfromtxt( args.input , delimiter = ',', skip_header=True)
    yvec = data[:, 3]
    if args.inverse:
        yvec = 0 - yvec 
    print("mean %s" % yvec.mean())
    pylab.subplot(2, 1, 1)
    pylab.plot( yvec, label = 'Raw' )
    pylab.plot( [ yvec.mean() ] * len(yvec) )
    mean = yvec.mean()
    yvec = yvec - mean
    std = yvec.std()
    print("[INFO] Standard deviation: %s" % std )
    # Now get the turns
    turns = get_turns( yvec )
    turns = filter(lambda x: accept_turn(x, mean), turns)
    csvOutfile = '%s_turns.csv' % (args.input)
    pngOutfile = '%s_turns.png' % (args.input)
    with open( csvOutfile, 'w' ) as csvF:
        csvF.write("location,amplitude,width\n")
        for t in turns:
            line = '%s,%s,%s\n' % t
            csvF.write( line )
    print('[INFO] Wrote csv data to %s' % csvOutfile)
    pylab.savefig( pngOutfile )
    print('[INFO] Wrote png file to %s' % pngOutfile)

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Analyze turns'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', '-i'
        , required = True
        , help = 'Input file'
        )
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument('--inverse', '-inv'
        , required = False
        , action = 'store_true'
        , help = 'Help'
        )
    parser.add_argument( '--debug', '-d'
        , required = False
        , default = 0
        , type = int
        , help = 'Enable debug mode. Default 0, debug level'
        )
    parser.add_argument('--min_width', '-mw'
        , required = False
        , default = 2
        , help = 'Help'
        )
    parser.add_argument('--min_amplitude', '-ma'
        , required = False
        , default = 5
        , help = 'Help'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
