"""helper.py: 

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
import math
import brian2 as _b_

def spikes_in_interval( monitor, simtime, interval ):
    print('[INFO] Binning spikes in interval of %s second' % interval)
    spike_dict = monitor.spike_trains()
    results = {}
    for k in spike_dict:
        result = []
        spikeTrain = spike_dict[k]
        space = np.arange(0, simtime, interval)
        if len(space) < 2:
            continue
        intervals = []
        for i, e in enumerate(space[1:]):
            intervals.append((space[i], space[i+1]))
        intervals.append( (space[-1], simtime) )
        for (start, stop) in intervals:
            a = np.where( spikeTrain > start*_b_.second)
            b = np.where( spikeTrain < stop*_b_.second)
            spikes = spikeTrain[np.intersect1d(a, b)]
            result.append(spikes)
        results[k] = result
    return results
