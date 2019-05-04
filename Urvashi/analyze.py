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
import matplotlib.pyplot as plt
plt.style.use('seaborn-talk')
import scipy.fftpack as fft
import pywt
import analytic_wfm
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

    axFFT.psd(y, NFFT=2048, Fs=fs_, noverlap=56) #, detrend='linear')
    axFFT.set_xscale('log')

    # Band pass
    extract_osci(x, y1)

def extract_osci(x, y):
    sos = butter_bandpass(lowcut=10, highcut=100, order=20)
    ySmooth = scipy.signal.sosfilt(sos, y)
    ySmooth -= ySmooth.mean()
    ySmooth = ySmooth / ySmooth.max()
    ax2.plot(x, ySmooth, alpha=0.8)

    # peak detection. Anything faster than 10ms is bogus.
    drive = smooth(ySmooth, 20e-3)
    drive = drive - drive.mean()
    drive = drive / max(drive.max(), -drive.min())
    ax2.plot(x, drive)
    maxP, minP = analytic_wfm.peakdetect(drive, x, delta=10e-3)
    pI, pV = zip(*maxP)
    ax2.plot(pI, pV, 'k.')

    # Estimate frequency.
    driveT = np.diff(pI)
    print(driveT)
    print(np.mean(driveT))

    
    #  yMoreSmooth = yMoreSmooth - yMoreSmooth.mean()
    #  u, s = np.mean(yMoreSmooth), np.std(yMoreSmooth)
    #  thres = u + 0.5*s
    #  yMoreSmooth[(yMoreSmooth > thres)] = 1
    #  yMoreSmooth[(yMoreSmooth < -thres)] = -1
    #  yMoreSmooth[yMoreSmooth < 0.0 ] = -1e-2
    #  drive = yMoreSmooth
    #  ax2.plot(x, drive, alpha=0.8)

    axFFT1.psd(ySmooth, Fs=fs_)
    axFFT1.set_xscale('log')

def process(df):
    tvec = df['Time']
    y1 = df['Trace 0']
    if True:
        a = int(32.2/dt_)
        b = a+60000
        x, y = tvec[a:b], y1[a:b]
    else:
        x, y = tvec, y1
    analyze(x, y)

    #plot_axis(ax1, tvec, y1)

    #y1[ y1 <= np.mean(y1)] = np.mean(y1)
    #y1 = smooth(y1, 200e-3)
    #plot_axis(ax2, tvec, y1)

    plt.tight_layout()
    plt.savefig(f'{__file__}.png')

def main():
    df = pd.read_csv(sys.argv[1])
    process(df)

if __name__ == '__main__':
    main()

