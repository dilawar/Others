#!/bin/bash
if [ ! -d $1 ]; then
    echo "Directory $1 not found"
    exit
fi
find $1 -type f -path "*Left*.csv" -print0 | xargs -0 -I file ./turns_in_swim.py \
    -i file --inverse

