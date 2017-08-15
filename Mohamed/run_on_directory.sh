#!/usr/bin/env bash

DIR=$1
files=`find $DIR -name "*.oib"`
for f in ${files}; do
    echo "Analyzing $f"
    python ./compute_cell_intensity.py $f
done
