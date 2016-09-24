#!/usr/bin/env python

import re,glob
import sys
from collections import defaultdict
from collections import Counter

args_ = None

def main( ):
    with open( args_.gidfile, "r") as f :
        gids = f.read()

    out_fd = open( args_.pfamda, "w" )

    gid_dict = defaultdict( list )
    domain_arch_dict={}

    with open( args_.hmmout, 'r' ) as f :
        for hmm_line  in f :
            if (re.match('#',hmm_line)) :
                continue
            hmm_cols = hmm_line.split()
            query_name = hmm_cols[3]
            gid = query_name.split('|')[1]
            if gid in gids:
                pfam_accession_desc = hmm_cols[0]
                pfam_accession_id = hmm_cols[1]
                tlen = int(hmm_cols[2])
                env_cord_from = int(hmm_cols[19])
                env_cord_to = int(hmm_cols[20])
                target_cov = float((env_cord_to - env_cord_from))/float(tlen)
                if (target_cov > 0.7) :
                    gid_dict[gid].append( ( pfam_accession_id, env_cord_from, env_cord_to ) )

    uniqueDas = defaultdict( int )
    with open( args_.domain, 'w' ) as f:
        for k in gid_dict:
            values = sorted( gid_dict[k], key = lambda x: x[2] )
            col1 =  "~".join([ x[0] for x in values ])
            col2 =  "~".join([ "%s-%s" % x[1:3] for x in values ])
            uniqueDas[ col1 ] += 1
            f.write( "%s\t%s\n" % (col1, col2) )
    print( '[INFO] Wrote to %s' % args_.domain )
    uniqueDaCount = Counter( uniqueDas )
    with open( args_.uniqueDA, 'w' ) as uf:
        for k in uniqueDaCount:
            uf.write( '%s\t%s\n' % (k, uniqueDaCount[k]) )
    print( '[INFO] Done writing uniqueDA to %s' % args_.uniqueDA )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A tool to extract unique domain architecture")
    parser.add_argument('-i', dest="hmmout",required = True,help="Input HMM SCAN out")
    parser.add_argument('-g', dest="gidfile",required = True,help="GID file")
    parser.add_argument('-p', dest="pfamda",default="pfamda_out.txt",help="Output PFAM DA file")
    parser.add_argument('-d', dest="domain",default="da_out.txt",help="Output DA file")
    parser.add_argument('-u', dest="uniqueDA",default="unique_da_out.txt",help="Output unique DA file")
    args_ = parser.parse_args()
    main(  )
    print( '[INFO] All done' )
