import sys
import numpy as np 
import pylab as pl
import numpy.random as rand  # Random number generation module


data = np.loadtxt(sys.argv[1])

#print data

# Simple example to produce a histogram of the errors
pl.hist(data[:], bins=50)
pl.savefig('outputHistogram.pdf')
pl.show()


