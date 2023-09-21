# ATB to LAMMPS file converter

<a href="webp">
  <img src="luteolin_C15H10O6/luoteolin.webp" align="right" width="30%"/>
</a>

Use Python and [Moltemplate](https://www.moltemplate.org/) to convert 
files from the [ATB repository](https://atb.uq.edu.au/) to LAMMPS format. 
Several examples are given here, including [luteolin](luteolin_C15H10O6/) 
(video on the right), [methane](methane_CH4), or [ethanol](ethanol_C2H5OH). 

## Use

### Extract system.lt file

```
python3 extract_system_lt.py KIR7_allatom_optimized_geometry.lt
```

### Execute moltemplate

```
moltemplate.sh system.lt
```

### Create clean system

```
python3 clean_system.py
```

### Delete extra files

```
rm -r output_ttree
rm system.*
```

### run LAMMPS

```
lmp -in input.lammps
```
