#!/bin/bash

python3 extract_system_lt.py KIR7_allatom_optimized_geometry.lt

moltemplate.sh system.lt

python3 clean_system.py

rm -r output_ttree
rm system.*
