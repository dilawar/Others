#!/usr/bin/env python3

"""analyze.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import pyabf
import matplotlib.pyplot as plt
try:
    plt.style.use('seaborn-talk')
except Exception as e:
    pass
import scipy.fftpack as fft
import scipy.signal
import numpy as np
import pandas as pd

fs_ = 20e3
dt_ = 1.0/fs_

plt.figure(figsize=(15, 8))
gridSize = (3, 3)
ax1 = plt.subplot2grid(gridSize, (0,0), colspan=2)
axFFT = plt.subplot2grid(gridSize, (0,2), rowspan=1)
axFFT1 = plt.subplot2grid(gridSize, (1,2), rowspan=1)
ax2 = plt.subplot2grid( gridSize, (1,0), colspan=2)

#  axImgImg = plt.subplot2grid( gridSize, (2,1), colspan=1, rowspan=2)

def abf_to_dfs(files):
    dfs = {}
    for f in files:
        abf = pyabf.ABF(f)
        abf.setSweep(0)
        df = pd.DataFrame()
        header = abf.headerText
        for sl in abf.sweepList:
            abf.setSweep(sl)
            x, y = abf.sweepX, abf.sweepY
            df[ f'Time' ] = x
            df[ f'Trace{sl}' ] = y
        dfs[f] = df
    return dfs


def plot_axis(ax, x, y):
    ax.plot(x, y)

def butter_bandpass(lowcut=0.001, highcut=1000, order=6):
    nyq = 0.5 * fs_
    low = lowcut/nyq
    high = highcut/nyq
    print( f"[INFO ] Bandpass filter: {low} to {high}" )
    sos = scipy.signal.butter(order, [low, high], btype='band', output='sos')
    return sos

def butter_lowpass(highcut=100, order=3):
    nyq = 0.5 * fs_
    high = highcut/nyq
    b, a = scipy.signal.butter(order, [high], btype='low')
    return b, a

def smooth(x, winsize=10e-3):
    N = int(winsize//dt_)
    print( f"[INFO ] Convolution window size is {N}" )
    return np.convolve(x, np.ones(N)/N, 'same')

def do_cwt(t, y, ax):
    from wavelets import WaveletAnalysis
    wa = WaveletAnalysis(y.values, dt=dt_)
    power = wa.wavelet_power
    scales = wa.scales
    T, S = np.meshgrid(t, scales)
    ax.contourf(T, S, power, 100)
    #  ax.set_yscale('log')

def analyze(x, y):
    ax1.plot(x, y, alpha=0.8)
    y1 = y.copy()
    thres = y1.mean() #+ y1.std()
    #  y1[y1<thres] = thres
    y1 = y1 - y1.min()
    y1 = y1 / y1.max()
    ax11 = ax1.twinx()
    ax11.plot(x, y1, alpha=0.8, color='red')

    axFFT.psd(y, NFFT=2048, Fs=fs_, noverlap=56) #, detrend='linear')
    axFFT.set_xscale('log')


    sos = butter_bandpass(lowcut=10, highcut=100, order=20)
    ySmooth = scipy.signal.sosfilt(sos, y1)
    ax2.plot(x, ySmooth, alpha=0.8)

    axFFT1.psd(ySmooth, Fs=fs_)
    axFFT1.set_xscale('log')

    # Convolve with morlet wavelet.
    #ySmoothMorlet = np.convolve(x, scipy.signal.morlet(100, w=5), 'same')
    #ax2.plot(x, ySmoothMorlet, alpha=0.8, label='Morlet')


    #  do_cwt(x, y, axImgReal)

    ## CWT
    #widths = np.arange(10e-3/dt_, 100e-3/dt_)
    #cwtmatr = scipy.signal.cwt(y, lambda n, w:scipy.signal.morlet(n, w=10), widths)
    #im = axImgReal.imshow(np.real(cwtmatr)
    #        , aspect='auto')
    #  plt.colorbar(im, ax=axImgReal)


def process(df):
    tvec = df['Time']
    y1 = df['Trace0']
    a = int(32.2/dt_)
    b = a+6000
    x, y = tvec[a:b], y1[a:b]
    #  x, y = tvec, y1
    analyze(x, y)

    #plot_axis(ax1, tvec, y1)

    #y1[ y1 <= np.mean(y1)] = np.mean(y1)
    #y1 = smooth(y1, 200e-3)
    #plot_axis(ax2, tvec, y1)

    plt.tight_layout()
    plt.savefig(f'{__file__}.png')

def main(args):
    dfs = abf_to_dfs(args.input_abf)
    for f, df in dfs.items():
        print(df.columns)
        process(df)

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Subthreshold oscillations.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input-abf', '-i'
        , required = True, nargs = '+'
        , help = 'Input file (abf format)'
        )
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument( '--debug', '-d'
        , required = False
        , default = 0
        , type = int
        , help = 'Enable debug mode. Default 0, debug level'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main(args)

