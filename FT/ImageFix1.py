from scipy import misc
import matplotlib.pyplot as plt
import numpy as np

def getCrossCorrelation(im, i):
	l1 = np.fft.fft(im[i])
	l2 = np.fft.fft(np.roll(im, 1, axis=0)[i])
	
	corr = np.fft.ifft(np.multiply(l1, np.conjugate(l2)))
	return corr.real

fn = str(input("File : "))
im = misc.imread(fn)
im_s = misc.imread(fn)

#cols = len(im)
#rows = len(im[0])

#im = np.delete(im, np.arange(rows)[:10], 1)

#im = np.delete(im, np.arange(rows)[(rows-11):], 1)
#im_s = np.copy(im)


iminus = np.roll(np.arange(len(im)), 1)
corr = np.zeros((len(im), len(im[0])))

for i in range(len(im)-1):
	j = (len(im)-1)-i
	corr[j] = getCrossCorrelation(im_s, j)
	im_s[iminus[j]] = np.roll(im_s[iminus[j]], np.argmax(corr[j]))

plt.subplot(121), plt.imshow(im, cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(im_s, cmap=plt.cm.gray)


plt.show()

