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
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    #mpl.style.use( ['bmh', 'fivethirtyeight'] )
    mpl.style.use( 'ggplot')
except Exception as e:
    pass
import scipy.fftpack as fft
import analytic_wfm
import scipy.signal
import numpy as np
import pandas as pd

fs_ = 20e3
dt_ = 1.0/fs_


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


def plot_time_series(x, y, drive, peaks, outfile):
    #  plt.figure(figsize=(15, 10))
    gridSize = (2, 3)
    ax1 = plt.subplot2grid(gridSize, (0,0), colspan=2)
    axFFT1 = plt.subplot2grid(gridSize, (0,2), rowspan=1)
    ax2 = plt.subplot2grid( gridSize, (1,0), colspan=2, sharex=ax1)
    axFs = plt.subplot2grid(gridSize, (1,2), rowspan=1)

    ax1.plot(x, y)
    axFFT1.psd(y, Fs=fs_)
    axFFT1.set_xscale('log')
    axFFT1.set_ylabel('PSD')


    ax2.plot(x, drive, lw=0.5)
    ax2.set_xlabel('Time (sec)')
    xP, yP = zip(*peaks)
    ax2.plot(xP, yP, 'k.')

    # Plot the histogram of frequencies.
    ts = np.diff(xP)
    fs = 1/ts
    axFs.hist(fs, bins=np.arange(fs.min(), fs.max(), 1))
    axFs.set_xlabel('Frequency (Hz)')
    

    plt.tight_layout()
    plt.savefig( outfile )

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

def analyze_time_series(x, y):
    y1 = y.copy()
    y1 = y1 - y1.min()
    y1 = y1 / y1.max()
    return extract_osci(x, y1)

def extract_osci(x, y):
    sos = butter_bandpass(lowcut=10, highcut=100, order=20)
    ySmooth = scipy.signal.sosfilt(sos, y)
    ySmooth -= ySmooth.mean()
    ySmooth = ySmooth / ySmooth.max()

    # peak detection. Anything faster than 10ms is bogus.
    drive = smooth(ySmooth, 20e-3)
    drive = drive - drive.mean()
    drive = drive / max(drive.max(), -drive.min())
    drive[drive < 0.5*drive.std()] = 0
    maxP, minP = analytic_wfm.peakdetect(drive, x, delta=10e-3)
    pI, pV = zip(*maxP)

    # Estimate frequency.
    driveT = np.diff(pI)
    driveF = 1.0 / driveT
    return drive, maxP, driveF

def process(df, f):
    tvec = df['Time']
    plot = True
    for c in df.columns:
        if c == 'Time':
            continue
        y1 = df[c]
        x, y = tvec, y1
        drive, peaks, fs = analyze_time_series(x, y)
        if plot:
            outfile = f"{f}.{c}.png"
            plot_time_series(x, y, drive, peaks, outfile)

def main(args):
    dfs = abf_to_dfs(args.input_abf)
    for f, df in dfs.items():
        process(df, f)

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

