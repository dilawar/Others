"""thres.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import random
import numpy as np
import itertools
import re
import networkx as nx
import subprocess


def randomly_assign_parameter( n, g ):
    for s, t in g.in_edges( n ):
        ex = random.gauss( 1, 0.5 )
        ih = random.gauss( -1, 0.5 )
        w = random.choice( [ex, ih] )
        g.edge[s][t]['weight'] = w

def create_random_network( g ):
    for n in g.nodes( ):
        if 'n' in n:
            randomly_assign_parameter( n, g )
            g.node[n]['threshold'] = random.gauss( 0, 1.0 )

def compute_expr( g, output ):
    # assign input.
    expr = ''
    nrns = g.predecessors( output )
    assert len( nrns ) == 1
    nrn = nrns[-1]
    ins = g.predecessors( nrn )
    ws = [ g.edge[x][nrn]['weight'] for x in ins ]
    e = '+'.join( [ '((%s)*(%s))' % (w,i) for w, i in zip( ws, ins) ] )
    thres = g.node[nrn]['threshold']
    expr = '(1 if (%s>%s) else 0)' % ( e, thres) 

    expandable = list( filter( lambda x: 'o' in x, ins ) )
    if not expandable:
        return expr

    for o in expandable:
        subexpr = compute_expr( g, o )
        expr = expr.replace( o, subexpr )

    return expr

def decimal( inputs ):
    val = 0
    for i, v in enumerate( inputs ):
        val += v * (2**i)
    return val

def compute( expr, dval ):
    res = expr
    for k, v in dval.items( ):
        res =  res.replace( k, str(v) )
    #print( res )
    return eval( res )

def truth_table( expr ):
    tt = [ ]
    minterms = [ ]
    ports = list( set( re.findall( r'i\d+', expr )))
    for inputs in itertools.product( [0,1], repeat = len(ports) ):
        dval = dict( zip(ports, inputs) )
        v = compute( expr, dval )
        if v == 1:
            minterms.append( decimal( inputs ) ) 
        tt.append( ' '.join(map(str,inputs)) + ' ' + str(v) )
    return '\n'.join(tt), sorted( minterms )

def print_network( g ):
    #nx.nx_pydot.write_dot( g, sys.stdout )
    weights = { }
    thresh = { }
    for n1, n2 in g.edges( ):
        if 'n' in n2:
            weights[ (n1,n2) ] = g.edge[n1][n2]['weight']
            thresh[ n2 ] = g.node[n2]['threshold']

    for (n1,n2), w in weights.items( ):
        print( '%s --> %s: %03.3f' % ( n1, n2, w) )

    for nrn in thresh:
        print( '%s: %s' % (nrn, thresh[nrn]) )
    return weights, thresh
    

def main( ):
    template = nx.drawing.nx_agraph.read_dot( sys.argv[1] )
    N = 10000
    for i in range( N ):
        g = template.copy( )
        create_random_network( g )
        if i == 0:
            print_network( g )
        if i % 1000 == 0:
            print( '%d steps are done out of %d' % (i, N) )
        expr = compute_expr( g, 'O' )
        tt, minTerms = truth_table( expr )
        if minTerms == [1,2]:
            print_network( g )
            print( '---')
            print( tt )
            print( minTerms )
            print( '---' )

if __name__ == '__main__':
    main()

