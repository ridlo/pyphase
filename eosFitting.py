#!/usr/bin/python -tt
"""EOS Fitting"""
from pylab import *     # -> numpy as np
from scipy.optimize import leastsq

### Function
def Quadratic(params, vol):
    """Quadratic equation"""
    a, b, c = params
    e = a*vol**2 + b*vol + c
    return e

def Murnaghan(params, vol):
    """Murnaghan EOS"""
    E0, B0, BP, V0 = params
    E = E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1.) + 1.) - V0*B0/(BP-1.)
    return E

#! add another eos function


# objective function to be minimized
def objective(pars, y, x, eosfunction):
    err = y - eosfunction(pars, x)
    return err

# generate guess
def genGuess(data):
    """
    the parabola does not fit the data very well, 
        but we can use it as initial guess
    E   = aV^2 + bV + c
    V0 -> dE/dV = 0
    B  -> V0*(d^2E/dV^2)
    """
    v, e = data; a, b, c = polyfit(v, e, 2)
    v0 = -b/(2*a)
    e0 = a*v0**2 + b*v0 + c
    b0 = 2*a*v0
    bP = 4.
    guess = [e0, b0, bP, v0]
    return guess

# main function
def eos(data, eosfunction):
    """
    data            two column (volume, energy)
    eosfunction     name of EOS function to be fitted
                    has to be written before
    """
    x0 = genGuess(data)
    v, e = data
    eospars, cov, infodict, mesg, ier = leastsq(objective, x0, args=(e,v,eosfunction), full_output=True)
    return eospars



### read file
# read file with nfefn.data format
def read_file(filename):
    f = open(filename, 'r')
    x, y = [], []
    for line  in f:
        line = line.strip().split()
        x.append(float(line[0]))
        y.append(float(line[3]))
    f.close()
    x, y = np.array(x), np.array(y)
    return [x, y]


if __name__ == '__main__':

    filename = 'lattice_opt_k20.txt'
    x, y = read_file(filename)
    v, e = 0.25*(2*x)**3, y
    data = [v, e]
    murnpars = eos(data, Murnaghan)
    #a, b, c = polyfit(v, e, 2)

    filename1 = 'lattice_opt_k30.txt'
    x1, y1 = read_file(filename1)
    v1, e1 = 0.25*(2*x1)**3, y1
    data1 = [v1, e1]
    murnpars1 = eos(data1, Murnaghan)

    filename2 = 'lattice_opt_k40.txt'
    x2, y2 = read_file(filename2)
    v2, e2 = 0.25*(2*x2)**3, y2
    data2 = [v2, e2]
    murnpars2 = eos(data2, Murnaghan)

    filename3 = 'lattice_opt_k50.txt'
    x3, y3 = read_file(filename3)
    v3, e3 = 0.25*(2*x3)**3, y3
    data3 = [v3, e3]
    murnpars3 = eos(data3, Murnaghan)

    vfit = np.linspace(min(v),max(v),100)
    plot(v,e,'ro')
    plot(v1,e1,'ro')
    plot(v2,e2,'ro')
    plot(v3,e3,'ro')
    #plot(vfit, a*vfit**2 + b*vfit + c,'--',label='Parabolic fit')
    plot(vfit, Murnaghan(murnpars, vfit), label='cutoff_wf = 20Ry')
    plot(vfit, Murnaghan(murnpars1, vfit), label='cutoff_wf = 30Ry')
    plot(vfit, Murnaghan(murnpars2, vfit), label='cutoff_wf = 40Ry')
    plot(vfit, Murnaghan(murnpars3, vfit), label='cutoff_wf = 50Ry')
    xlabel('Volume (Bohr$^3$)')
    ylabel('Energy (Ha)')
    legend(loc='best')
    grid(True)
    show()
