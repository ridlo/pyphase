#!/usr/bin/python -tt
# author: ridlo w. wibowo

import sys
import os
import shutil

def read_inputfile(ifile):
    try:
        os.path.isfile(ifile)
    except:
        print sys.argv[0], "ERROR: no such file, ", ifile
    
    # read ifile
    with open(ifile, 'r') as f:
        file_names = f.readline().strip()
        file_input = f.readline().strip()
        params = f.readline().strip().split()
        par = params[0]
        mi  = float(params[1])
        mx  = float(params[2])
        ic  = float(params[3])
        change_after = f.readline() 
        lines = []
        for line in f:
            lines.append(line)

    return [file_names, file_input, par, mi, mx, ic, change_after, lines]

def scf_copier(ifile, case):
    data = read_inputfile(ifile)
    file_names = data[0]; file_input = data[1]
    par = data[2]; mi = data[3]; mx = data[4]; ic = data[5]
    change_after = data[6]; lines = data[7]
    
    val = mi; softening = 0.000001
    mx = mx + softening
    while val <= mx:
        # create subdir
        d = case+'_%g' % val
        if os.path.isdir(d):
            shutil.rmtree(d)
            print 'remove directory ', d

        os.mkdir(d); print 'make new dir ', d
        os.chdir(d); print 'open dir ', d

        # copy file input
        shutil.copy('../'+file_names, './') 
        print 'copy ', file_names, ' to ', d
        shutil.copy('../'+file_input, './')
        print 'copy ', file_input, ' to ', d

        # change file input
        ifile = open(file_input, 'r')
        
        # temporary file
        tmp_file = file_input+'.tmp'
        ofile = open(tmp_file, 'w')
        
        ifile = ifile.readlines()               # memory consuming, but its Ok 
        number_of_lines = range(len(ifile))     # hell
        for i in number_of_lines:
            ofile.write(ifile[i])
            if ifile[i] == change_after:
                for j in range(len(lines)):
                    ifile.pop(i+1)
                    number_of_lines.pop(-1)     # hell again.. 
                    newline = lines[j].replace(par, str(val))
                    ofile.write(newline)
         
        ofile.close()
        shutil.move(tmp_file, file_input)
        os.chdir('../')
        val += ic

#def run_program()

#def olah() 
           
if __name__ == '__main__':
    try:
        scf_copier(sys.argv[1], sys.argv[2])
    except:
        print "Error: no input\n"
        print "Usage: ", sys.argv[0], " <file input> <subdir firstname>"
        example_file = """file_names.data
input_scf_Si.data
uc 5.0 5.26 0.025
    unit_cell{
       a_vector =  0.0000000000        uc        uc
       b_vector =  uc        0.0000000000        uc
       c_vector =  uc        uc        0.0000000000"""
        print "Example of file input:"
        print example_file
