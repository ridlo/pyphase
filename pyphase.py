#!/usr/bin/python -tt
__author__ = 'ridlo w. wibowo'
__copyright__ = 'ridlo.w.wibowo@gmail.com'
__date__ = '13/05/2013'

import scf_clone
import sys
import os
import commands

print 'Lattice Optimization Script for PHASE'
print '-------------------------------------'

def pyphase(ifile):
    params = scf_clone.read_inputfile(ifile)
    cmd = 'python scf_clone.py ' + ifile
    print 'running :', cmd
    os.system(cmd)

    cmd = 'python lattice_opt.py -d '+params[2]+' -m '+params[4]+' '+params[5]+' '+params[6]+' -ifile nfefn.data -ofile lattice_opt.txt -fit q -plot'
    print 'running: ', cmd
    os.system(cmd)
if __name__ == '__main__':
    if len(sys.argv) > 1:
            pyphase(sys.argv[1])
    else:
        print "ERROR: no input file"
        print "USAGE: ", sys.argv[0], " <inputfile> "; sys.exit(1)
