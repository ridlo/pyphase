#!/usr/bin/python -tt
import sys, math, os, shutil           

# default filename of input parameters:
ifile = 'ifile_scf_opt.data'

# default headname
case = 'scf_tmp'

# if any change
while len(sys.argv) > 1:
    option = sys.argv[1]; del sys.argv[1]
    if option == '-ifile':
        ifile = sys.argv[1]; del sys.argv[1]
    elif option == '-case':
        case = sys.argv[1]; del sys.argv[1]
    else:
        print sys.argv[0], ': invalid option', option
        sys.exit(1)

# check existence of ifile
try:
    os.path.isfile(ifile)
except:
    print sys.argv[0], " no input file"
    sys.exit(1)

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
    print "Error: 3th line in ", ifile
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

"""
# create a subdirectory
d = case                    # name of subdirectory
if os.path.isdir(d):         # does d exist?
    shutil.rmtree(d)        # yes, remove directory d
    print 'remove directory'

os.mkdir(d)                 # make new directory d
print 'make new directory'

os.chdir(d)                 # move to new directory d
print 'change directory to /'+case

# make a copy of input file in this new directory d
shutil.copy('../'+ifile1, './')
shutil.copy('../'+ifile2, './')

# change ifile1
f = open(ifile1, 'w')
f.write("""
#%(lv)g
#%(case)s
""" % vars())
f.close()

# change ifile2

print 'finish...'
"""
