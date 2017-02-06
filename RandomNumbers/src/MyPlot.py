import sys
import numpy as np 
import pylab as pl
import numpy.random as rand  # Random number generation module

file = sys.argv[1]
outfile = file + ".pdf"

data = np.loadtxt(file)

#print data

# Simple example to produce a histogram of the errors
pl.hist(data[:], bins=50)
pl.savefig(outfile)
pl.show()

