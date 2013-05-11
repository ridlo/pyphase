#!/usr/bin/python -tt
import sys
import math
import os
import shutil           


def scf_change(ifile, case, opt):
    # check existence of ifile
    try:
        os.path.isfile(ifile)
    except:
        print sys.argv[0], "ERROR: no input file"
        sys.exit(1)
    
    option = opt
    # check pwd
    pwd = os.getcwd()

    # read ifile
    f = open(ifile, 'r')
    ifile1 = f.readline()               # file_names.data
    ifile2 = f.readline()               # input_*.data
    par = f.readline().strip().split()  # parameter 

    try:
        var = par[0]
        mi = float(par[1])
        mx = float(par[2])
    except:
        print "ERROR: 3th line in ", ifile
        sys.exit(1)

    after = f.readline()
    value = mi
    while value <= mx:
        # create subdirectory
        d = case+'_%s_%g' % (var, value)    # name of subdir
        if os.path.isdir(d):                # does d exist?
            shutil.rmtree(d)                # yes, then remove d
            print 'remove directory ', d
    
        os.mkdir(d)                         # make new subdir d
        print 'make new directory ', d
        os.chdir(d)                         # change directory d
        print 'open directory ', d
        print 'we are in ', os.getcwd()

    shutil.copy('../'+ifile1, './')     # copy file to new dir
    shutil.copy('../'+ifile2, './')
    
    # change input file
    # change ifile2
    with open(ifile2, 'r') as file:
        data = file.readlines()

    for i in xrange(len(data)):
        if data[i] == after:
            data[i+1]
            



    f.close()



if __name__ == '__name__':
    
    # default filename of input parameters:
    ifile = 'ifile_scf_opt.data'
    
    # default headname
    case = 'scf_tmp'
    
    # commands line input
    while len(sys.argv) > 1:
        option = sys.argv[1]; del sys.argv[1]
        if option == '-ifile':
            ifile = sys.argv[1]; del sys.argv[1]
        elif option == '-case':
            case = sys.argv[1]; del sys.argv[1]
        else:
            print sys.argv[0], ': invalid option', option
            print 'USAGE: ', sys.argv[0], ' [option] [input]'
            sys.exit(1)



