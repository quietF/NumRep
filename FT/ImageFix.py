from scipy import misc
import matplotlib.pyplot as plt
import numpy as np

fn = str(input("File : "))
im = misc.imread(fn)
im_s = misc.imread(fn)

iplus = np.roll(np.arange(len(im)), -1)

FTim = np.fft.fft(im_s)
correl = np.fft.ifft(np.multiply(FTim, np.conjugate(np.roll(FTim, -1, axis=0))))

for i in range(len(im_s)):
	im_s[iplus[i]] = np.roll(im_s[iplus[i]], np.argmax(correl[i].real))

plt.subplot(121), plt.imshow(im, cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(im_s, cmap=plt.cm.gray)

plt.show()
