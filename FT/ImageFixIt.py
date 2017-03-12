import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

def getCrossCorrelationDownUp(im, i):
	line1 = np.fft.fft(im[i])
	line2 = np.fft.fft(np.roll(im, 1, axis=0)[i])
	corr = np.fft.ifft(np.multiply(line1, np.conj(line2)))
	print(np.argmax(corr.real))
	return corr.real

def getCrossCorrelationUpDown(im, i):
	line1 = np.fft.fft(im[i])
	line2 = np.fft.fft(np.roll(im, -1, axis=0)[i])
	corr = np.fft.ifft(np.multiply(line1, np.conjugate(line2)))
	return corr.real

fn = str(input("File : "))
im = misc.imread(fn)
im_s = np.copy(im)
im_DownUp = np.copy(im)
im_UpDown = np.copy(im)

iminus = np.roll(np.arange(len(im)), 1)
iplus = np.roll(np.arange(len(im)), -1)

#tune = 6

#for i in range(1, len(im)):
	#im_s[iminus[i]][:tune] = im_s[i][:tune]
	#im_s[iminus[i]][(len(im_s)+2-tune):] = im_s[i][(len(im_s)+2-tune):]
	#im_DownUp[iminus[i]][:tune] = im_DownUp[i][:tune]
	#im_DownUp[iminus[i]][(len(im)+2-tune):] = im_DownUp[i][(len(im)+2-tune):]

corrDownUp = np.zeros((len(im), len(im[0])))
corrUpDown = np.zeros((len(im), len(im[0])))

for i in range(len(im)-1):
	j = (len(im)-1)-i
	corrDownUp[j] = getCrossCorrelationDownUp(im_DownUp, j)
	im_DownUp[iminus[j]] = np.roll(im_DownUp[iminus[j]], np.argmax(corrDownUp[j]))
	corrUpDown[i] = getCrossCorrelationUpDown(im_UpDown, i)
	im_UpDown[iplus[i]] = np.roll(im_UpDown[iplus[i]], np.argmax(corrUpDown[i]))

plt.imshow(im_s, cmap=plt.cm.gray), plt.show()
plt.imshow(im_DownUp, cmap=plt.cm.gray), plt.show()
plt.imshow(im_UpDown, cmap=plt.cm.gray), plt.show()
