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
    failure, output = commands.getstatusoutput(cmd)
    if failure:
        print 'ERROR in running %s\n%s' % (cmd, output); sys.exit(1)

    cmd = 'python lattice_opt.py -d '+params[2]+' -m '+params[4]+' '+params[5]+' '+params[6]+' -ifile nfefn.data -ofile lattice_opt.txt -fit q -plot'
    print 'running: ', cmd
    failure, output = commands.getstatusouput(cmd)
    if failure:
        print 'ERROR in running %s\n%s' % (cmd, output); sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
            pyphase(sys.argv[1])
    else:
        print "ERROR: no input file"
        print "USAGE: ", sys.argv[0], " <inputfile> "; sys.exit(1)
