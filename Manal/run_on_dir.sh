#!/bin/bash - 
#===============================================================================
#
#          FILE: run_on_dir.sh
# 
#         USAGE: ./run_on_dir.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: 08/16/2016 02:13:11 PM
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
set -e 

if [[ $# -lt 1 ]]; then
    echo "USAGE $0 dirname"
    exit
fi

find "$1" -type f -name "*.mat" -print0 | xargs -0 -I file \
    python ./plot_trajectories.py -f file
