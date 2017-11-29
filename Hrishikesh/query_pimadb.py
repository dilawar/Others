#!/usr/bin/env python

"""query_pimadb.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
from bs4 import BeautifulSoup
import urllib2
import re

def query_db( q, idx ):
    url = 'http://caps.ncbs.res.in/cgi-bin/pimadb/show_result.py?pdb_id=%s' % q
    html = urllib2.urlopen( url ).read( )

    soup = BeautifulSoup( html, "lxml" )

    rows = [ ]
    for table in soup.find_all( 'table' ):
        for r in table.find_all( 'tr' ):
            tds = r.find_all( 'td' )
            if len( tds ) < 1:
                continue
            if re.match( r'^[A-Z]-[A-Z]', tds[0].text):
                rows.append( [ x.text.strip( ) for x in tds ] )
    
    for r in rows:
        x = r
        if len( idx ) > 0:
            x = [ r[i] for i in idx ]
        print( ' '.join( x ) )


def main( ):
    query = sys.argv[1]
    idx = [ ]
    if len( sys.argv ) > 2:
        idx = [ int(x) for x in sys.argv[2:] ]
    query_db( query, idx )

if __name__ == '__main__':
    main()
