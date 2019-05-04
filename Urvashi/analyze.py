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
import scipy.signal
import numpy as np
import pandas as pd

fs_ = 20e3
dt_ = 1.0/fs_

plt.figure(figsize=(15, 10))
gridSize = (4, 3)
ax1 = plt.subplot2grid(gridSize, (0,0), colspan = 2 )
axFFT = plt.subplot2grid(gridSize, (0,2))
ax2 = plt.subplot2grid( gridSize, (1,0), colspan = 2 )

axImgReal = plt.subplot2grid( gridSize, (2,0), colspan=2, rowspan=2)
#  axImgImg = plt.subplot2grid( gridSize, (2,1), colspan=1, rowspan=2)

def plot_axis(ax, x, y):
    ax.plot(x, y)

def butter_bandpass(lowcut=1, highcut=100, order=6):
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
    y1[y1<thres] = thres
    y1 = y1 - y1.min()
    y1 = y1 / y1.max()
    ax11 = ax1.twinx()
    ax11.plot(x, y1, alpha=0.8, color='red')

    axFFT.psd(y, NFFT=2048, Fs=fs_, noverlap=56) #, detrend='linear')
    axFFT.set_xscale('log')
    #  axFFT.set_xlim(0, 200)

    sos = butter_bandpass(lowcut=10, order=15)
    ySmooth = scipy.signal.sosfilt(sos, y1)
    ax2.plot(x, ySmooth, alpha=0.8)

    # Convolve with morlet wavelet.
    #ySmoothMorlet = np.convolve(x, scipy.signal.morlet(100, w=5), 'same')
    #ax2.plot(x, ySmoothMorlet, alpha=0.8, label='Morlet')


    do_cwt(x, y, axImgReal)

    ## CWT
    #widths = np.arange(10e-3/dt_, 100e-3/dt_)
    #cwtmatr = scipy.signal.cwt(y, lambda n, w:scipy.signal.morlet(n, w=10), widths)
    #im = axImgReal.imshow(np.real(cwtmatr)
    #        , aspect='auto')
    #  plt.colorbar(im, ax=axImgReal)


def process(df):
    tvec = df['Time']
    y1 = df['Trace 0']
    a = int(32.2/dt_)
    b = a+6000
    x, y = tvec[a:b], y1[a:b]
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

