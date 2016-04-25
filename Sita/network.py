"""network.py: 

Construct network of habenula

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

from brian2 import *
import networkx as nx
import helper
import pylab 
import spike_to_gcamp as s2g

# Construct LHB
nNeuronsInLHB = 20 # 00
# Fraction of LHB neurons which are inhibitory
inhibitoryFraction = 0.5

# Synaptic weights
lhbExcSynapticWeight = 1.62
lhbInhibSynapticWeight = 9     # Should be positive



# Model of LHB neurons.
tau = 10*ms
lhbEqs = '''
dv/dt = (ge+gi-(v+49*mV))/(20*ms) : volt
dge/dt = -ge/(5*ms) : volt
dgi/dt = -gi/(10*ms) : volt

'''

print('[INFO] Constructing LHB with %s neurons' % nNeuronsInLHB )
print('[INFO]  Eq : %s' % lhbEqs )
lhb = NeuronGroup(nNeuronsInLHB, lhbEqs, threshold='v>-49.05*mV', reset='v=-60*mV') 
lhb.v = -60*mV

# Inhibitory group
lhbInhib = lhb[0:int(inhibitoryFraction*nNeuronsInLHB)]
# Excitatory group.
lhbExc = lhb[int(inhibitoryFraction*nNeuronsInLHB):]

# Make synapses in LHB
excSynapses = Synapses( lhbExc, lhb, pre='ge+=%f*mV' % lhbExcSynapticWeight)
excSynapses.connect( True, p = 0.02 )    # p is the probability of release

inhSynapse = Synapses( lhbInhib, lhb, pre='gi-=%f*mV' % lhbInhibSynapticWeight)
inhSynapse.connect( True, p = 0.02 )

lhbMonitor = SpikeMonitor( lhb )

def main( ):
    runTime = 5
    run( runTime*second )
    pylab.subplot(2, 1, 1)
    plot( lhbMonitor.t, lhbMonitor.i, '.')

    binInterval = 0.5
    nspikesDict = helper.spikes_in_interval( lhbMonitor, runTime, binInterval)

    dtForFluroscenceComputation = 0.01
    rows = []
    for k in nspikesDict.keys():
        print('[DEBUG] ======== Bins for neuron %s' % k )
        vec = nspikesDict[k]
        print('         %s' % vec)
        r = np.zeros( runTime / dtForFluroscenceComputation )
        for _bin in vec:
            _bin = np.sort( _bin )
            if _bin.shape[0] > 0:
                r = s2g.spikes_to_fluroscence(r, _bin, dtForFluroscenceComputation)
        rows.append( r )
    pylab.subplot(2, 1, 2)
    pylab.plot( rows[4] )
    pylab.plot( rows[5] )
    pylab.savefig( './spikes_raster.png' )

if __name__ == '__main__':
    main()

