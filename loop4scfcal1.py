#!/usr/bin/python -tt
import sys, os, commands

try:
    option_name = sys.argv[1]
    mi = float(sys.argv[2])
    mx = float(sys.argv[3])
    ic = float(sys.argv[4])
except IndexError:
    print "Usage: ", sys.argv[0], \
    "parameter min max increment [ scfcal1.py options]"
    sys.exit(1)
except ValueError:
    print "Input a number please.."
    sys.exit(1)

scfcal1_options = ' '.join(sys.argv[5:])

value = mi
while value <= mx:
    case = 'scf_tmp_%s_%g' % (option_name, value)
    cmd = 'python scfcal1.py %s -%s %g -case %s' % (scfcal1_options, option_name, value, case)
    print 'running ', cmd
    failure, output = commands.getstatusoutput(cmd)
    value += ic

print 'finish...'
