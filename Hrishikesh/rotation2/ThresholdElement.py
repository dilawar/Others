"""ThresholdElement.py: 

Threshold Element.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import numpy as np
import random
import itertools

class Neuron( ):

    def __init__(self, weights, threshold ):
        self.threshold = threshold
        self.weights = weights
        self.nInputs = len( self.weights )
        self.output = 0 # random.choice( [0, 1] )

    def __repr__( self ):
        msg = ', '.join( ['i%d*%.2f' % (i,w) for (i,w) in enumerate(self.weights) ] )
        msg = 'Threhold function: ' + msg + ' >= %.2f' % self.threshold
        return msg

    def apply( self, inputs ):
        """Take next step.
        """
        self.inputs = inputs
        total = sum([ i * w for i, w in zip( self.weights, self.inputs ) ])
        if total >= self.threshold:
            self.output = 1.0 
        else:
            self.output = 0.0


def main( ):
    h1 = Neuron( [0.1,0.1], 0.2 )
    h2 = Neuron( [0.1,0.2], 0.2 )

    for inputs in itertools.product( [0,1], [0,1] ):
        print( 'Applying %s' % str(inputs) )
        h1.apply( inputs )
        print( ' H1 outout : %f' % h1.output )
        h2.apply( inputs )
        print( ' H2 outout : %f' % h2.output )


if __name__ == '__main__':
    main()
