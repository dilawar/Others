"""spike_to_gcamp.py: 

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
import pylab
import math

def spike_to_fluroscence( vec, start_time, dt, rise_time = 0.2, fall_half_time = 0.6):
    N = len(vec)
    startIdx = int(start_time / dt)
    t = np.arange(0, (N*dt - start_time), dt)
    f1 = np.clip(t / rise_time, 0, 1)
    f2 = np.clip(np.exp( - (t-rise_time)/ fall_half_time), 0, 1)
    prefix = np.zeros( start_time / dt )
    func = np.hstack( (prefix, f1 + f2 - 1.0) )
    return np.array(func, dtype=np.float)

def spikes_to_fluroscence( init_activity, spike_at, dt, **kwargs):
    rise_time = kwargs.get('rise_time', 0.2)
    fall_half_time = kwargs.get('fall_half_time', 0.6)
    for s in spike_at:
        res = spike_to_fluroscence( init_activity, s, dt
                , rise_time
                , fall_half_time
                )
        init_activity += res
    return init_activity

def main():
    test = [ 0.1, 0.2, 0.21 ]
    dt = 1e-2
    camp = np.zeros( 4/dt )
    camp = spikes_to_fluroscence( camp, test, dt)
    pylab.plot( camp )
    pylab.show()



if __name__ == '__main__':
    main()
