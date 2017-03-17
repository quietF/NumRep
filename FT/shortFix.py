import sys
sys.path.insert(1, '/usr/local/lib/python3.5/dist-packages/')

import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

#fn = str(input("File : ")) # uncomment this to enable user interaction.
fn = "desync1.pgm"

image = misc.imread(fn) # np.array((columns, rows))
FTimage = np.fft.fft(image[:]) # dft of each line in image

auto_xcorrelation = np.fft.ifft(np.multiply(FTimage[1:], np.conjugate(FTimage[1:]))).real # auto cross correlation of each line

image_up = np.roll(image, 1, axis=0) # image_up[i] = image[i+1] (with periodic boundary conditions)
FTimage_up = np.fft.fft(image_up[:])
xcorrelation = np.fft.ifft(np.multiply(FTimage[1:], np.conjugate(FTimage_up[1:]))).real # cross correlation of each line with the one above it

x = np.arange(len(image)-1)

plt.plot(x, np.max(auto_xcorrelation, axis=1), 'b', x, np.max(xcorrelation, axis=1), 'r')
plt.show()

differences = np.max((auto_xcorrelation[:] - xcorrelation[:]), axis=1)
condition = (np.abs(differences)>np.average(differences))

shift = np.argmax(xcorrelation, axis=1)
shift = shift * condition[:]
axes = np.full((len(shift)), 1, dtype=int)

for i in range(1, len(image)):
    image[i] = np.roll(image[i], -shift[i-1])

print("{0}, {1}".format(len(shift[:]), len(image[1:])))

#image[1:] = np.roll(image[1:], shift[:], axis=axes[:])

plt.imshow(image, cmap=plt.cm.gray)
plt.show()

plt.plot(x, np.abs(differences), 'b', x, np.full(len(differences), np.average(differences)), 'r')
plt.show()