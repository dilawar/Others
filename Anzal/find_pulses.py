__author__           = "Dilawar Singh"
__email__            = "dilawar.s.rajput@gmail.com"

from pathlib import Path
import sys
import neo
import numpy as np
import matplotlib.pyplot as plt

def channel_name_to_index(reader, channel_name):
    for signal_channel in reader.header["signal_channels"]:
        if channel_name == signal_channel[0]:
            return int(signal_channel[1])

def find_ttl_start(trace, N: int = 10):
    sr = trace.sampling_rate
    data = np.array(trace)
    data -= data.min()
    data /= data.max()
    pulses = []
    for i, x in enumerate(data[::N]):
        if (i + 1) * N >= len(data):
            break
        y = data[(i+1)*N]
        if x < 0.2 and y > 0.75:
            pulses.append((i*N, i*N/float(sr)))
    return pulses

def main(abfpath: Path):
    reader = neo.io.AxonIO(abfpath)
    block = reader.read_block(signal_group_mode="split-all")
    fid = channel_name_to_index(reader, 'FrameTTL')
    pulses = []
    for sid, segment in enumerate(block.segments):
        y = segment.analogsignals[fid]
        pulses.append(find_ttl_start(y, N=3))
    return pulses

if __name__ == "__main__":
    pulses = main(sys.argv[1])
    for p in pulses:
        print('\n'.join([f"{x[0]},{x[1]}" for x  in p]))
