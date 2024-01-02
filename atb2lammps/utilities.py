import os
import shutil
import numpy as np

def detect_lt_file(molecule_folder):
    """Identify the name of the lt file containing the molecule information"""
    lt_file = None
    for filename in os.listdir(molecule_folder):
        if (filename.split(".")[1] == "lt") & (filename.split("_")[0] != "GROMOS"):
            if len(filename.split("_")) > 3:
                lt_file = filename
    if lt_file is None:
        print("WARNING: lt file not found")
    return lt_file

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        cpt = 0
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return cpt
            cpt += 1
    return None

def write_system_lt(molecule_folder, file_name):
    start_line = check_if_string_in_file(molecule_folder + "/" + file_name,'system.lt')
    end_line = check_if_string_in_file(molecule_folder + "/" + file_name,'= new')
    with open(molecule_folder + '/' + file_name, 'r') as read_obj:
        cpt = 0
        system_lt = []
        for line in read_obj:
            if (cpt > start_line-1) & (cpt <= end_line):
                system_lt.append(line[3:]) 
            cpt += 1
    with open(molecule_folder + '/' + "system.lt", "w") as text_file:
        text_file.write(''.join(system_lt))

def delete_extra_files(molecule_folder):
    if os.path.exists(molecule_folder + '/system.lt'):
        os.remove(molecule_folder + '/system.lt')
    if os.path.exists(molecule_folder + '/output_ttree'):
        shutil.rmtree(molecule_folder + '/output_ttree/')
    if os.path.exists(molecule_folder + '/system.data'):
        os.remove(molecule_folder + '/system.data')
    if os.path.exists(molecule_folder + '/system.in.init'):
        os.remove(molecule_folder + '/system.in.init')
    if os.path.exists(molecule_folder + '/system.in.settings'):
        os.remove(molecule_folder + '/system.in.settings')
    if os.path.exists(molecule_folder + '/run.in.EXAMPLE'):
        os.remove(molecule_folder + '/run.in.EXAMPLE')

def clean_moltemplate_files(folder):
    # read settings
    with open(folder + '/system.in.settings', 'r') as read_obj:
        all_mass = []
        all_pair_coeff = []
        all_bond = []
        all_angle = []
        all_dihedral = []
        all_improper = []
        for line in read_obj:
            if ('mass' in line) & ('#' not in line):
                _, _, rest = line.partition("mass")
                splitted_line = rest[:-1].split(' ',20)[1:]
                splitted_line = list(filter(None, splitted_line))
                ids = np.int32(splitted_line[0])
                mass = np.float32(splitted_line[1])
                all_mass.append(np.array([ids,mass]))
            if ('pair_coeff' in line) & ('#' not in line):
                _, _, rest = line.partition("pair_coeff")
                splitted_line = rest[:-1].split(' ',20)[1:]
                splitted_line = list(filter(None, splitted_line))
                ids1 = np.int32(splitted_line[0])
                ids2 = np.int32(splitted_line[1])
                eps = np.float32(splitted_line[2])
                sig = np.float32(splitted_line[3])
                all_pair_coeff.append(np.array([ids1,ids2,eps,sig]))
            if ('bond_coeff' in line) & ('#' not in line):
                _, _, rest = line.partition("bond_coeff")
                splitted_line = rest[:-1].split(' ',20)[1:]
                splitted_line = list(filter(None, splitted_line))
                ids = np.int32(splitted_line[0])
                k = np.float32(splitted_line[1])
                r0 = np.float32(splitted_line[2])
                all_bond.append(np.array([ids,k,r0]))
            if ('angle_coeff' in line) & ('#' not in line):
                _, _, rest = line.partition("angle_coeff")
                splitted_line = rest[:-1].split(' ',20)[1:]
                splitted_line = list(filter(None, splitted_line))
                ids = np.int32(splitted_line[0])
                k = np.float32(splitted_line[1])
                theta0 = np.float32(splitted_line[2])
                all_angle.append(np.array([ids,k,theta0]))
            if ('dihedral_coeff' in line) & ('#' not in line):
                _, _, rest = line.partition("dihedral_coeff")
                splitted_line = rest[:-1].split(' ',20)[1:]
                splitted_line = list(filter(None, splitted_line))
                ids = np.int32(splitted_line[0])
                k = np.float32(splitted_line[1])
                n = np.int32(splitted_line[2])
                phi0 = np.int32(splitted_line[3])
                all_dihedral.append(np.array([ids,k,n,phi0]))
            if ('improper_coeff' in line) & ('#' not in line):
                _, _, rest = line.partition("improper_coeff")
                splitted_line = rest[:-1].split(' ',20)[1:]
                splitted_line = list(filter(None, splitted_line))
                ids = np.int32(splitted_line[0])
                k = np.float32(splitted_line[1])
                xi0 = np.float32(splitted_line[2])
                all_improper.append(np.array([ids,k,xi0]))
    all_mass = np.array(all_mass)
    all_pair_coeff = np.array(all_pair_coeff)
    all_bond = np.array(all_bond)
    all_angle = np.array(all_angle)
    all_dihedral = np.array(all_dihedral)
    all_improper = np.array(all_improper)

    # read data
    with open(folder + '/system.data', 'r') as read_obj:
        cpt = 0
        for line in read_obj:
            if ('atoms' in line) & ('#' not in line):
                rest, _, _ = line.partition("atoms")
                nb_atoms = np.int32(rest)
            if ('bonds' in line) & ('#' not in line):
                rest, _, _ = line.partition("bonds")
                nb_bonds = np.int32(rest)
            if ('angles' in line) & ('#' not in line):
                rest, _, _ = line.partition("angles")
                nb_angles = np.int32(rest)
            if ('dihedrals' in line) & ('#' not in line):
                rest, _, _ = line.partition("dihedrals")
                nb_dihedrals = np.int32(rest)
            if ('impropers' in line) & ('#' not in line):
                rest, _, _ = line.partition("impropers")
                nb_impropers = np.int32(rest)
            if ('Atoms' in line):
                start_Atoms_section = cpt
            if ('Bonds' in line):
                start_Bonds_section = cpt          
            if ('Angles' in line):
                start_Angles_section = cpt
            if ('Dihedrals' in line):
                start_Dihedrals_section = cpt
            if ('Impropers' in line):
                start_Impropers_section = cpt
            cpt += 1
            
    # in case there are no angle, no dihedrals, or/and no impropers
    if nb_angles == 0:
        start_Angles_section = cpt
    if nb_dihedrals == 0:
        start_Dihedrals_section = cpt
    if nb_impropers == 0:
        start_Impropers_section = cpt
    end_file = cpt

    # read molecule
    if nb_atoms>0:
        with open(folder + '/system.data', 'r') as read_obj:
            cpt = 0
            Atoms = []
            for line in read_obj:
                if (cpt > start_Atoms_section+1) & (cpt < start_Bonds_section-1):
                    splitted_line = line[:-1].split(' ',20)
                    splitted_line = list(filter(None, splitted_line))
                    Atoms.append(np.float32(splitted_line)) 
                cpt += 1
        Atoms = np.array(Atoms)
    if nb_bonds>0:
        with open(folder + '/system.data', 'r') as read_obj:
            cpt = 0
            Bonds = []
            for line in read_obj:
                if (cpt > start_Bonds_section+1) & (cpt < start_Angles_section-1):
                    splitted_line = line[:-1].split(' ',20)
                    splitted_line = list(filter(None, splitted_line))
                    Bonds.append(np.float32(splitted_line)) 
                cpt += 1
        Bonds = np.array(Bonds)
    else:
        Bonds = None
    if nb_angles>0:
        with open(folder + '/system.data', 'r') as read_obj:
            cpt = 0
            Angles = []
            for line in read_obj:
                if (cpt > start_Angles_section+1) & (cpt < start_Dihedrals_section-1):
                    splitted_line = line[:-1].split(' ',20)
                    splitted_line = list(filter(None, splitted_line))
                    Angles.append(np.float32(splitted_line)) 
                cpt += 1
        Angles = np.array(Angles)
    else:
        Angles = None
    if nb_dihedrals>0:
        with open(folder + '/system.data', 'r') as read_obj:
            cpt = 0
            Dihedrals = []
            for line in read_obj:
                if (cpt > start_Dihedrals_section+1) & (cpt < start_Impropers_section-1):
                    splitted_line = line[:-1].split(' ',20)
                    splitted_line = list(filter(None, splitted_line))
                    Dihedrals.append(np.float32(splitted_line))             
                cpt += 1
        Dihedrals = np.array(Dihedrals)
    else:
        Dihedrals = None
    if nb_impropers>0:
        with open(folder + '/system.data', 'r') as read_obj:
            cpt = 0
            Impropers = []
            for line in read_obj:
                if (cpt > start_Impropers_section+1) & (cpt < end_file-1):
                    splitted_line = line[:-1].split(' ',20)
                    splitted_line = list(filter(None, splitted_line))
                    Impropers.append(np.float32(splitted_line))             
                cpt += 1
        Impropers = np.array(Impropers)
    else:
        Impropers = None
        
    # filter the force field value 
    # keep only the relevant values
    filtered_mass = []
    convert_atoms = []
    cpt = 1
    for ids, value in all_mass:
        if np.sum(np.unique(Atoms.T[2]) == ids) > 0:
            filtered_mass.append(np.array([ids,value]))
            convert_atoms.append([cpt, ids])
            cpt += 1
    filtered_mass = np.array(filtered_mass)
    convert_atoms = np.array(convert_atoms)

    filtered_pair_coeff = []
    for ids1, ids2, value1, value2 in all_pair_coeff:
        if (np.sum(np.unique(Atoms.T[2]) == ids1) > 0) & (np.sum(np.unique(Atoms.T[2]) == ids2) > 0):
            filtered_pair_coeff.append(np.array([ids1, ids2, value1, value2]))
    filtered_pair_coeff = np.array(filtered_pair_coeff)

    if nb_bonds>0:
        filtered_bond = []
        convert_bonds = []
        cpt = 1
        for ids, value1, value2 in all_bond:
            if np.sum(np.unique(Bonds.T[1]) == ids) > 0:
                filtered_bond.append(np.array([ids,value1, value2]))
                convert_bonds.append([cpt, ids])
                cpt += 1
        filtered_bond = np.array(filtered_bond)
        convert_bonds = np.array(convert_bonds)
    else:
        filtered_bond = None

    if nb_angles>0:
        filtered_angle = []
        convert_angles = []
        cpt = 1
        for ids, value1, value2 in all_angle:
            if np.sum(np.unique(Angles.T[1]) == ids) > 0:
                filtered_angle.append(np.array([ids,value1, value2]))
                convert_angles.append([cpt, ids])
                cpt += 1
        filtered_angle = np.array(filtered_angle)
        convert_angles = np.array(convert_angles)
    else:
        filtered_angle = None

    if nb_dihedrals>0:
        filtered_dihedral= []
        convert_dihedrals = []
        cpt = 1
        for ids, value1, value2, value3 in all_dihedral:
            if np.sum(np.unique(Dihedrals.T[1]) == ids) > 0:
                filtered_dihedral.append(np.array([ids,value1, value2, value3]))
                convert_dihedrals.append([cpt, ids])
                cpt += 1
        filtered_dihedral = np.array(filtered_dihedral)
        convert_dihedrals = np.array(convert_dihedrals)
    else:
        filtered_dihedral = None

    if nb_impropers>0:
        filtered_improper= []
        convert_impropers = []
        cpt = 1
        for ids, value1, value2 in all_improper:
            if np.sum(np.unique(Impropers.T[1]) == ids) > 0:
                filtered_improper.append(np.array([ids,value1, value2]))
                convert_impropers.append([cpt, ids])
                cpt += 1
        filtered_improper = np.array(filtered_improper)
        convert_impropers = np.array(convert_impropers)
    else:
        filtered_improper = None
        
    if nb_atoms>0:
        # convert ids to be 1,2,3,4...
        for new_ids, old_ids in convert_atoms:
            where = np.where(filtered_mass.T[0] == old_ids)
            filtered_mass[where,0] = new_ids

            where = np.where(filtered_pair_coeff.T[0] == old_ids)
            filtered_pair_coeff[where,0] = new_ids

            where = np.where(filtered_pair_coeff.T[1] == old_ids)
            filtered_pair_coeff[where,1] = new_ids    

            where = np.where(Atoms.T[2] == old_ids)
            Atoms[where,2] = new_ids
    if nb_bonds>0:
        for new_ids, old_ids in convert_bonds:
            where = np.where(filtered_bond.T[0] == old_ids)
            filtered_bond[where,0] = new_ids

            where = np.where(Bonds.T[1] == old_ids)
            Bonds[where,1] = new_ids
    if nb_angles>0:
        for new_ids, old_ids in convert_angles:
            where = np.where(filtered_angle.T[0] == old_ids)
            filtered_angle[where,0] = new_ids

            where = np.where(Angles.T[1] == old_ids)
            Angles[where,1] = new_ids
    if nb_dihedrals>0:
        for new_ids, old_ids in convert_dihedrals:
            where = np.where(filtered_dihedral.T[0] == old_ids)
            filtered_dihedral[where,0] = new_ids

            where = np.where(Dihedrals.T[1] == old_ids)
            Dihedrals[where,1] = new_ids
    if nb_impropers>0:
        for new_ids, old_ids in convert_impropers:
            where = np.where(filtered_improper.T[0] == old_ids)
            filtered_improper[where,0] = new_ids

            where = np.where(Impropers.T[1] == old_ids)
            Impropers[where,1] = new_ids
    return nb_atoms, nb_bonds, nb_angles, nb_dihedrals, nb_impropers, \
        Atoms, Bonds, Angles, Dihedrals, Impropers, \
        filtered_mass, filtered_pair_coeff, filtered_bond, \
        filtered_angle, filtered_dihedral, filtered_improper

def write_lammps_data(molecule_folder):
    nb_atoms, nb_bonds, nb_angles, nb_dihedrals, nb_impropers, \
         Atoms, Bonds, Angles, Dihedrals, Impropers, \
         filtered_mass, filtered_pair_coeff, filtered_bond, \
         filtered_angle, filtered_dihedral, filtered_improper = clean_moltemplate_files(molecule_folder)
    
    # detect if molecule has partial charges
    if (np.max(Atoms.T[3]) == 0) & (np.min(Atoms.T[3]) == 0):
        no_charge = True
    else:
        no_charge = False

    f = open(molecule_folder + "/single_molecule.data", "w")
    f.write('# LAMMPS data file \n')
    f.write('# Created using atb2lammps \n')
    f.write('# https://github.com/simongravelle/atb2lammps\n\n')
    if nb_atoms>0:
        f.write(str(nb_atoms)+' atoms\n')
    if nb_bonds>0:
        f.write(str(nb_bonds)+' bonds\n')
    if nb_angles>0:
        f.write(str(nb_angles)+' angles\n')
    if nb_dihedrals>0:
        f.write(str(nb_dihedrals)+' dihedrals\n')
    if nb_impropers>0:
        f.write(str(nb_impropers)+' impropers\n')
    f.write('\n')
    if nb_atoms>0:
        f.write(str(np.int32(np.max(Atoms.T[2])))+' atom types\n')
    if nb_bonds>0:
        f.write(str(np.int32(np.max(Bonds.T[1])))+' bond types\n')
    if nb_angles>0:
        f.write(str(np.int32(np.max(Angles.T[1])))+' angle types\n')
    if nb_dihedrals>0:
        f.write(str(np.int32(np.max(Dihedrals.T[1])))+' dihedral types\n')
    if nb_impropers>0:
        f.write(str(np.int32(np.max(Impropers.T[1])))+' improper types\n')
    f.write('\n')
    f.write('-25 25 xlo xhi\n')
    f.write('-25 25 ylo yhi\n')
    f.write('-25 25 zlo zhi\n')
    if nb_atoms>0:
        f.write('\n')
        f.write('Atoms\n')
        f.write('\n')
        for nlin in Atoms:
            for cpt_col, col in enumerate(nlin):
                if cpt_col < 3:
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n')
    if nb_bonds>0:
        f.write('\n')
        f.write('Bonds\n')
        f.write('\n')
        for nlin in Bonds:
            for cpt_col, col in enumerate(nlin):
                f.write(str(np.int32(col))+' ')
            f.write('\n')
    if nb_angles>0:
        f.write('\n')
        f.write('Angles\n')
        f.write('\n')
        for nlin in Angles:
            for cpt_col, col in enumerate(nlin):
                f.write(str(np.int32(col))+' ')
            f.write('\n')
    if nb_dihedrals>0:
        f.write('\n')
        f.write('Dihedrals\n')
        f.write('\n')
        for nlin in Dihedrals:
            for cpt_col, col in enumerate(nlin):
                f.write(str(np.int32(col))+' ')
            f.write('\n')
    if nb_impropers>0:
        f.write('\n')
        f.write('Impropers\n')
        f.write('\n')
        for nlin in Impropers:
            for cpt_col, col in enumerate(nlin):
                f.write(str(np.int32(col))+' ')
            f.write('\n')
    f.close()

    return no_charge

def write_parm(molecule_folder):
    nb_atoms, nb_bonds, nb_angles, nb_dihedrals, nb_impropers, \
         Atoms, Bonds, Angles, Dihedrals, Impropers, \
         filtered_mass, filtered_pair_coeff, filtered_bond, \
         filtered_angle, filtered_dihedral, filtered_improper = clean_moltemplate_files(molecule_folder)

    # Write parameter file
    f = open(molecule_folder + "/parm.lammps", "w")
    f.write('# LAMMPS parameter file \n')
    f.write('# Created using atb2lammps \n')
    f.write('# https://github.com/simongravelle/atb2lammps\n\n')
    if nb_atoms>0:
        for nlin in filtered_mass:
            f.write('mass ')
            for cpt_col, col in enumerate(nlin):
                if cpt_col == 0:
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n')
        f.write('\n')
        for nlin in filtered_pair_coeff:
            f.write('pair_coeff ')
            for cpt_col, col in enumerate(nlin):
                if cpt_col < 2:
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n')
        f.write('\n')
    if nb_bonds>0:
        for nlin in filtered_bond:
            f.write('bond_coeff ')
            for cpt_col, col in enumerate(nlin):
                if cpt_col == 0:
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n') 
        f.write('\n') 
    if nb_angles>0:
        for nlin in filtered_angle:
            f.write('angle_coeff ')
            for cpt_col, col in enumerate(nlin):
                if cpt_col == 0:
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n')
        f.write('\n') 
    if nb_dihedrals>0:
        for nlin in filtered_dihedral:
            f.write('dihedral_coeff ')
            for cpt_col, col in enumerate(nlin):
                if (cpt_col == 0) | (cpt_col>1):
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n')
        f.write('\n') 
    if nb_impropers>0:
        for nlin in filtered_improper:
            f.write('improper_coeff ')
            for cpt_col, col in enumerate(nlin):
                if cpt_col == 0:
                    f.write(str(np.int32(col))+' ')
                else:
                    f.write(str(np.float32(col))+' ')
            f.write('\n')
        f.write('\n') 
    f.close()

def write_lammps_input(molecule_folder, no_charge):
    # Write lammps input file
    f = open(molecule_folder + "/single_molecule.lammps", "w")
    f.write('# LAMMPS input file \n')
    f.write('# Created using atb2lammps \n')
    f.write('# https://github.com/simongravelle/atb2lammps\n\n')
    f.write('boundary p p p\n')
    f.write('units real\n')
    f.write('atom_style full\n')
    f.write('bond_style harmonic\n')
    f.write('angle_style harmonic\n')
    f.write('dihedral_style harmonic\n')
    f.write('improper_style harmonic\n')
    f.write('pair_style lj/cut/coul/long 14\n')
    f.write('kspace_style pppm 1e-5\n')
    if no_charge:
        f.write('kspace_modify gewald 1.0\n')
    f.write('special_bonds lj 0.0 0.0 0.5 coul 0.0 0.0 1.0 angle yes dihedral yes\n')
    f.write('read_data single_molecule.data\n')
    f.write('include parm.lammps\n')
    f.write('minimize 1.0e-5 1.0e-7 1000 10000\n')
    f.write('reset_timestep 0\n')
    f.write('fix mynvt all nvt temp 300 300 100\n')
    f.write('timestep 1.0\n')
    f.write('dump mydmp all atom 1000 dump.lammpstrj\n')
    f.write('dump myimg all image 2000 molecule.*.ppm type type size 640 640 box no 0.1\n')
    f.write('thermo 1000\n')
    f.write('run 6000\n')
    f.close()
