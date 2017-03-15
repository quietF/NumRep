import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

def get_cross_correlation(image, line_number):
    '''
    :param image: np.array(rows, cols) of uint8 type
    :param line_number: int from 1 to rows
    :return: cross correlation between line #line_number and line #line_number-1
    '''
    base_line = np.fft.fft(image[line_number])
    compared_line = np.fft.fft(np.roll(image, 1, axis=0)[line_number])
    cross_correlation = np.fft.ifft(np.multiply(base_line, np.conjugate(compared_line)))
    return cross_correlation.real

def get_self_cross_correlation(image, line_number):
    '''
    :param image: np.array(rows, cols) of uint8 type
    :param line_number: int from 1 to rows
    :return: self cross correlation of line #line_number
    '''
    base_line = np.fft.fft(image[line_number])
    compared_line = np.fft.fft(image[line_number])
    cross_correlation = np.fft.ifft(np.multiply(base_line, np.conjugate(compared_line)))
    return cross_correlation.real

def clean_up(image_in):

    image_out = np.copy(image_in)
    copy_range = int(0.05 * len(image_out[0]))
    cross_correlation = np.zeros((len(image_out), len(image_out[0])))
    for i in range(1, len(image_out)):
        cross_correlation[i] = get_cross_correlation(np.roll(image_in, -1, axis=0), i)
        if np.argmax(cross_correlation[i]) != 0:
            #image_out[i] = np.roll(image_in, -1, axis=0)[i]
            image_out[i][:copy_range] = np.roll(image_in, 1, axis=0)[i][:copy_range]
            image_out[i][len(image_out[0])-copy_range:] = np.roll(image_in, 1, axis=0)[i][len(image_out[0])-copy_range:]

    return image_out

def get_avg_max_difference(image):

    avg_max_difference = 0
    cross_correlation = np.zeros((len(image), len(image[0])))
    self_cross_correlation = np.zeros((len(image), len(image[0])))

    for i in range(1, len(image)):

        cross_correlation[i] = get_cross_correlation(image, i)
        self_cross_correlation[i] = get_self_cross_correlation(image, i)
        avg_max_difference += np.abs(np.max(self_cross_correlation[i]) -
                                     self_cross_correlation[i][np.argmax(cross_correlation[i])]) / len(image)

    print(avg_max_difference)
    return avg_max_difference

#fn = str(input("File : "))
fn = "desync2.pgm"
im = misc.imread(fn)
im0 = np.copy(im)

avg_max_difference = get_avg_max_difference(im)

rubbish = int(0.01*len(im[0])/2)
print("rubbish: {0}".format(rubbish))

im = np.delete(im, np.s_[:rubbish], 1)
im = np.delete(im, np.s_[len(im[0])-rubbish:], 1)

cc = np.zeros((len(im), len(im[0])))
cc_max = np.zeros(len(im))

self_cc = np.zeros((len(im), len(im[0])))
self_cc_max = np.zeros(len(im))
self_cc_at_cc_max = np.zeros(len(im))

avg_max_difference = get_avg_max_difference(im)

for i in range(1, len(im)):
    cc[i] = get_cross_correlation(im, i)
    self_cc[i] = get_self_cross_correlation(im, i)
    self_cc_max[i] = np.max(self_cc[i])
    self_cc_at_cc_max[i] = self_cc[i][np.argmax(cc[i])]

    max_difference[i] = (self_cc_at_cc_max[i] - self_cc_max[i])

    if np.abs(max_difference[i]) > avg_max_difference:
        im[i] = np.roll(im[i], - np.argmax(cc[i]).astype(int))


plt.plot(np.abs(max_difference))
plt.show()

im = np.delete(im, np.s_[:rubbish], 1)
im = np.delete(im, np.s_[len(im[0])-rubbish:], 1)

plt.subplot(121), plt.imshow(im0, cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(im, cmap=plt.cm.gray)
plt.show()

im1 = clean_up(im)

plt.subplot(121), plt.imshow(im, cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(im1, cmap=plt.cm.gray)
plt.show()