# ATB-to-LAMMPS file converter

<a href="webp">
  <img src="molecules/luteolin_C15H10O6/luoteolin.png" align="right" width="30%"/>
</a>

Use Python and [Moltemplate](https://www.moltemplate.org/) to convert 
files from the [ATB repository](https://atb.uq.edu.au/) to LAMMPS format. 

## Full molecule list

- [nitrogen](molecules/nitrogen_N2)
- [methane](molecules/methane_CH4)
- [carbondioxide](molecules/carbondioxide_CO2)
- [decane](molecules/decane_C10H22)
- [luteolin](molecules/luteolin_C15H10O6)
- [ethane](molecules/ethane_C2H6)
- [acetronitrice](molecules/acetronitrice_C2H3N)
- [water](molecules/water_H2O)
- [ethanol](molecules/ethanol_C2H5OH)
- [toluene](molecules/toluene_C7H8)
- [propane](molecules/propane_C3H8)

## How to add a new molecule

### Save the files from the ATB

Within *molecules/*, create a folder with the format *name_formula/*, 
where name is the molecule name, and formula its chemical formula.

Save the two *.lt* files from the atb within *molecules/*.

### Run atb2lammps

From the *atb2lammps/* folder, run *execute_atp2lammps.py* using Python.
