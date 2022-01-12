import sys

file_name = sys.argv[1]

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        cpt = 0
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True, cpt
            cpt += 1
    return False, 0
    
_, start_line = check_if_string_in_file(file_name,'system.lt')

_, end_line = check_if_string_in_file(file_name,'= new')

with open(file_name, 'r') as read_obj:
    cpt = 0
    system_lt = []
    for line in read_obj:
        if (cpt > start_line-1) & (cpt <= end_line):
            system_lt.append(line[3:]) 
        cpt += 1
with open("system.lt", "w") as text_file:
    text_file.write(''.join(system_lt))
