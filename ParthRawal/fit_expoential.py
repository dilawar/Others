#!/usr/bin/env python3
# -*- coding: utf-8 -*-

    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import scipy.optimize as sco
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Args: pass 
args = Args()

def model(x, y, R, Pmax):
    return Pmax * (1- np.exp(-x/R))

def fit_exp(x, y):
    popt, pcov = sco.curve_fit(model, x, y)
    return popt

def method_fit(x, y, ax):
    popt = fit_exp(x, y)
    ax.plot( x, model(x, *popt), label=f'{c} fit')
    ax.legend()

def method_midR(x, y, ax):
    midY = (y.min() + y.max()) / 2.0
    rate = np.gradient(y, x)
    maxRateI = np.where(rate >= rate.max())[0][0]
    ax.plot(x, rate)
    print( f"[INFO ] Mid value {midY}, max rate {rate.max()} at {maxRateI}" )
    return max(rate), x[maxRateI], np.log(2)/np.log(1+rate) - x

def main():
    global args
    df = pd.read_csv( args.input )
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)
    tvec = df['Time(H)'][1:]
    print( f"[INFO ] Selecting columsn {args.ycols}" )
    
    if args.ycols == 'all':
        cols = df.columns[1:]
    else:
        cols = df.filter(regex=args.ycols).columns
    for c in cols:
        y = df[c][1:]
        ax1.plot( tvec, y, '-o', label = c )
        if args.method == 'fit':
            method_fit(tvec, y, ax1)
        elif args.method == 'midR':
            maxR, maxRT, doublingT = method_midR(tvec, y, ax2)
            ax2.plot( [maxRT], [maxR], 'ko' )
            ax3.semilogy(tvec, doublingT)
            #  ax3.set_xlim([0, 6])
            #  ax3.set_ylim([0,200])
        else:
            raise RuntimeError( f'Method {args.method} not supported' )
        
    plt.tight_layout()
    plt.savefig( f'{args.input}.png' )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Fit data with exponential'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', '-i'
        , required = True
        , help = 'Input data file (csv)'
        )
    parser.add_argument('--ycols', '-y'
        , required = True, type = str
        , help = 'Name of columns (csv)'
        )
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument('--method', '-m'
        , required = False, type=str, default = 'midR'
        , help = 'Which method fit|midR'
        )
    parser.add_argument( '--debug', '-d'
        , required = False
        , default = 0
        , type = int
        , help = 'Enable debug mode. Default 0, debug level'
        )
    parser.parse_args(namespace=args)
    main()

