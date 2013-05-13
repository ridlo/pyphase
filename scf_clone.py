#!/usr/bin/python -tt
__author__ = 'ridlo w. wibowo'
__copyright__ = 'ridlo.w.wibowo@gmail.com'
__date__ = '13/05/13'

import sys
import os
import shutil
import commands

def read_inputfile(ifile):
    """ read input file, restricted format"""
    try:
        os.path.isfile(ifile)
    except:
        print sys.argv[0], "ERROR: no such file, ", ifile
    
    # read ifile
    with open(ifile, 'r') as f:
        file_names = f.readline().strip()
        file_input = f.readline().strip()
        case       = f.readline().strip()
        params = f.readline().strip().split()
        par = params[0]
        mi  = float(params[1])
        mx  = float(params[2])
        ic  = float(params[3])
        change_after = f.readline() 
        lines = []
        for line in f:
            lines.append(line)

    return [file_names, file_input, case, par, mi, mx, ic, change_after, lines]

def scf_copier(ifile):
    """ generate folder, copy input file and modify it"""
    data = read_inputfile(ifile)
    file_names = data[0]; file_input = data[1]; case = data[2]
    par = data[3]; mi = data[4]; mx = data[5]; ic = data[6]
    change_after = data[7]; lines = data[8]
    
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

def run_program(ifile):
    """running program on each subdirectory"""
    print 'Using parallel computer?'
    ans = raw_input('(Y/N) [N]: ')
    
    data = read_inputfile(ifile)
    case = data[2]; mi = data[4]; mx = data[5]; ic = data[6]
    
    if (ans == '' or ans == 'N' or ans == 'n'):
        print 'Where is your executable phase program?'
        srcFile = raw_input("(absolute path or relative to SUBDIR): ")

        val = mi; softening = 0.000001
        mx = mx + softening
        while val <= mx:
            d = case+'_%g' % val
            os.chdir(d); print 'open dir ', d
            os.symlink(srcFile, './phase'); print 'make soft link here', srcFile
            cmd = './phase'
            print 'running PHASE'
            failure, output = commands.getstatusoutput(cmd);
            if failure:
                print 'running PHASE program is failed\n%s\n%s' % \
                (cmd, output); sys.exit(1)

            os.chdir('../'); print 'back to', os.getcwd()
            val += ic

    elif (ans == 'Y' or ans == 'y'):
        print 'Where is your jobfile (qsub)?'
        srcFile = raw_input("(absolute path or relative to SUBDIR): ")

        val = mi; softening = 0.000001
        mx = mx + softening
        while val <= mx:
            d = case+'_%g' % val
            os.chdir(d); print 'open dir ', d
            os.symlink(srcFile, './parallel.sh'); print 'make soft link here', srcFile
            cmd = 'qsub parallel.sh'
            print 'running PHASE in parallel'
            failure, output = commands.getstatusoutput(cmd)
            if failure:
                print 'running PHASE program using parallel is failed\n%s\n%s' % \
                (cmd, output); sys.exit(1)
            os.chdir('../'); print 'back to', os.getcwd()
            val += ic

    else:
        print "Your answer is cute,  exit" 
        sys.exit(1)

def run(ifile):
    """ run PHASE program or not? """
    print "Run program on each subdirectory?"
    ans = raw_input('(Y/N) [Y]: ')
    
    if ans == '' or ans == 'Y' or ans == 'y':
        run_program(ifile)
    elif ans == 'N' or ans == 'n':
        print 'Ok, fighting!'; sys.exit(1)
    else:
        print "Your answer is weird..."; run(ifile)

           
if __name__ == '__main__':
    example_file = """file_names.data
input_scf_Si.data
scf_tmp_lv
uc 5.0 5.26 0.025
    unit_cell{
       a_vector =  0.0000000000        uc        uc
       b_vector =  uc        0.0000000000        uc
       c_vector =  uc        uc        0.0000000000"""
    
    usage = "USAGE    : "+ sys.argv[0] +" <file input>"
    
    print "--- Lattice Optimization Script ---"
    print "make sure you have change 'file_names.data' and make inputfile for this script"
    # read input file and make clone
    if len(sys.argv) > 1:     
        try:        
            scf_copier(sys.argv[1])
        except:
            print 'error in inputfile'; print example_file; sys.exit(1)
    else:
        print 'Error: no input file\n'
        print usage; print example_file; sys.exit(1)
    
    # if you need to run PHASE program
    run(sys.argv[1])
