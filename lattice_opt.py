#!/usr/bin/python -tt
__author__ = 'ridlo w. wibowo'
__copyright__ = 'ridlo.w.wibowo@gmail.com'
__date__ = '13/05/13'

import sys
import commands
import matplotlib.pyplot as plt

def read_nfefn(ifile):
    """read file nfefn.data"""
    f = open(ifile, 'r')
    f.readline()    # read header
    data = f.readline()
    f.close()
    return data

def read_iter(case, mi, mx, ic, ifilename, ofilename):
    """iteration of reading nfefn.data in subdir and write it on file"""
    f = open(ofilename, 'w')
    mi = float(mi); mx = float(mx); ic = float(ic)
    val = mi
    mx = mx+ic
    while val <= mx:
        ifile = '%s_%g/' % (case, val) + ifilename
        print "read ", ifile
        data = read_nfefn(ifile)
        line = str(val) + ' ' + data
        f.write(line)
        val += ic
    f.close()

def read_output(filedata):
    """read output file of extracted data"""
    # read extracted data
    f = open(filedata, 'r')
    par = []; eng = []
    for line in f:
        line = line.strip().split()
        par.append(float(line[0]))
        eng.append(float(line[3]))
    f.close()
    return [par, eng]

#-------------- Fitting Function --------------#
# 1. Quadratic function
def quadratic(filedata, plot):
    """ fitting using quadratic function a + b*x + c*x**2"""
    print "read ", filedata    
    data = read_output(filedata)
    # make file input for gnuplot
    f = open('lattice_opt.gnuplot', 'w')

    f.write("""# gnuplot input file
f(x) = a + b*x + c*x**2.
fit f(x) "%s" using 1:4 via  a,b,c
x_min = -b/(2*c)
y_min = a + b*x_min + c*x_min**2.
set print "lattice_opt_quadratic.data"
print 'x_opt    y_opt
print x_min, y_min
""" % filedata)
    
    if (plot):
        label = """
set terminal png
set output 'lattice_opt.png'
set title "Lattice Optimization"
set xlabel "Lattice parameter [Bohr]"
set ylabel "Energy [Ha]"
ti = sprintf("f(x) = %.3fx**2 + %.3fx + %.3f", c, b, a)
"""
        plotting = label+'plot "'+ filedata + '" u 1:4 w p pt 6 ps 0.7 title "data", f(x) title ti'        
        f.write(plotting)
    
    f.close()
    # fitting and plot using gnuplot
    cmd = 'gnuplot lattice_opt.gnuplot' # command to run
    print "run gnuplot.."    
    failure, output = commands.getstatusoutput(cmd)
    if failure:
        print 'ERROR in running gnuplot for fitting and plot\n%s\n%s' % \
        (cmd, output); sys.exit(1)
    
#------------- 2. Murnaghan, and Birch-Murnaghan [N/A]

def read_opt(ifile)
    # read ifile
    f = open(ifile, 'r')
    f.readline()      # read header
    data_opt = f.readline().strip().split()
    par = float(data_opt[0]); eng = float(data_opt[1])
    f.close()    
    return [par, eng]


if __name__ == '__main__':
    usage = """
    USAGE   : """+ sys.argv[0] +""" [option] <input>
    OPTION  :
        -d  <directory first name>
        -m  <min> <max> <increment>            
        -ifile <input filename: "nfefn.data">          
        -ofile <output filename>
        -fit <function>
            function: 
                Q   quadratic
                M   Murnaghan       [N/A]
                BM  Birch-Murnaghan [N/A]           
    Example : python """+ sys.argv[0]+""" -d scf_tmp_lv 5 5.25 0.025 -ifile nfefn.data -ofile lattice_opt.txt -fit q -plot"""
    
    if len(sys.argv) == 1:
        print usage
        sys.exit(1)
    
    fit = 'q'   
    plt = False 
    while len(sys.argv) > 1:
        option = sys.argv[1]; del sys.argv[1]
        if option == '-d':
            case = sys.argv[1]; del sys.argv[1]
        elif option == '-m':
            mi = sys.argv[1]; del sys.argv[1]
            mx = sys.argv[1]; del sys.argv[1]
            ic = sys.argv[1]; del sys.argv[1]
        elif option == '-ifile':
            ifile = sys.argv[1]; del sys.argv[1]
        elif option == '-ofile':
            ofile = sys.argv[1]; del sys.argv[1]
        elif option == '-fit':
            fit = sys.argv[1]; del sys.argv[1]
        elif option == '-plot':
            plt = True
        else:
            print sys.argv[0], ': invalid option ', option
            print usage
            sys.exit(1)
    try:
        read_iter(case, mi, mx, ic, ifile, ofile)
    except:
        print "ERROR in collecting and writing data"
        sys.exit(1)

    if fit == 'q' or fit == 'Q' or fit == 'quadratic':
        quadratic(ofile, plt)
        print "See 'fit.log' and/or 'lattice_opt.png'... have a nice day!"
        print "Optimum value: ", read_opt('lattice_opt_quadratic.data') 
