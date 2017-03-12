from scipy import misc
import matplotlib.pyplot as plt
import numpy as np

def getCrossCorrelation(im, i):
	l1 = np.fft.fft(im[i])
	l2 = np.fft.fft(np.roll(im, -1, axis=0)[i])
	
	corr = np.fft.ifft(np.multiply(l1, np.conjugate(l2)))
	return corr.real

fn = str(input("File : "))
im = misc.imread(fn)
im_s = misc.imread(fn)

iplus = np.roll(np.arange(len(im)), -1)
corr = np.zeros((len(im), len(im[0])))

for i in range(len(im)-1):
	corr[i] = getCrossCorrelation(im_s, i)
	im[i][np.argmax(corr[i])] = 0;
	im_s[iplus[i]] = np.roll(im_s[iplus[i]], np.argmax(corr[i]))

im_good = np.copy(im_s)



plt.subplot(131), plt.imshow(im, cmap=plt.cm.gray)
plt.subplot(132), plt.imshow(im_s, cmap=plt.cm.gray)
plt.subplot(133), plt.imshow(im_good, cmap=plt.cm.gray)


plt.show()
