#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: bash $(basename $0) atb-lammps-geometry.lt"
    exit 1
fi

# extract system
atbgeometry=$1
python3 extract_system_lt.py $atbgeometry

# call moltemplate
moltemplate.sh system.lt

# generate clean lammps input files
python3 clean_system.py

# remove unecessary files
rm -r output_ttree
rm system.*
