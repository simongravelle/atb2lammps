# atb2lammps
Convert files from the ATB repository to LAMMPS format

### Extract system.lt file

python3 extract_system_lt.py KIR7_allatom_optimized_geometry.lt

### Execute moltemplate

moltemplate.sh system.lt
