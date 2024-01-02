import numpy as np




# Write lammps input file
f = open("input.lammps", "w")
f.write('# LAMMPS input file \n')
f.write('# Created using atb2lammps \n')
f.write('# https://github.com/simongravelle/atb2lammps\n\n')
f.write('boundary p p p\n')
f.write('units real\n')
f.write('atom_style      full\n')
f.write('bond_style      harmonic\n')
f.write('angle_style     harmonic\n')
f.write('dihedral_style  harmonic\n')
f.write('improper_style  harmonic\n')
f.write('pair_style      lj/cut/coul/long 14\n')
f.write('kspace_style    pppm 0.0001\n')
f.write('special_bonds lj 0.0 0.0 0.5 coul 0.0 0.0 1.0 angle yes dihedral yes\n')
f.write('read_data data.lammps\n')
f.write('include parm.lammps\n')
f.write('minimize 1.0e-5 1.0e-7 1000 10000\n')
f.write('reset_timestep 0\n')
f.write('fix mymom all momentum 100 linear 1 1 1 angular\n')
f.write('fix mynvt all nvt temp 300 300 100\n')
f.write('timestep 1.0\n')
f.write('dump mydmp all atom 1000 dump.lammpstrj\n')
f.write('thermo 1000\n')
f.write('run 50000\n')
f.write('write_data data.equilibrium\n')
f.close()
