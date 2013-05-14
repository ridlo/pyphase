#!/usr/bin/python -tt
__author__ = 'ridlo w. wibowo'
__copyright__ = 'ridlo.w.wibowo@gmail.com'
__date__ = '13/05/2013'

import scf_clone
import sys
import os
import commands
import time

print 'Lattice Optimization Script for PHASE'
print '-------------------------------------'
print 'Make sure you have input file for this script, modify the file_names.data and have PHASE program path'

def clone(ifile):
    start = time.time()
    cmd = 'python scf_clone.py ' + ifile
    print 'running :', cmd; os.system(cmd)
    elapsed = time.time() - start
    print 'total running time: ', elapsed, ' second'

def pyphase(ifile, lo):
    params = scf_clone.read_inputfile(ifile)
    if lo:	
        cmd = 'python lattice_opt.py -d '+params[2]+' -m '+str(params[4])+' '+str(params[5])+' '+str(params[6])+' -ifile nfefn.data -ofile lattice_opt.txt -fit q -plot'
        print 'running: ', cmd; os.system(cmd)
    else:
        clone(ifile)

if __name__ == '__main__':
    if sys.argv[2] == '-lo':
        pyphase(sys.argv[1], True)
    elif sys.argv[2] == '-clone':
        pyphase(sys.argv[1], False)
    else:
        print "ERROR: no input file, and choice"
        print "USAGE: ", sys.argv[0], " <inputfile> [-lo or -clone]"; sys.exit(1)
