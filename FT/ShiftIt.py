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

def clean_up(image):

    image_out = np.copy(image)
    copy_range = int(0.01 * len(image_out[0]))
    print(copy_range)
    cross_correlation = np.zeros((len(image_out), len(image_out[0])))

    for i1 in range(1, len(image_out)-1):
        cross_correlation[i1] = get_cross_correlation(image_out, i1)

        if np.argmax(cross_correlation[i1]) != 0:
            #image_out[i1] = np.roll(image_in, -1, axis=0)[i1]
            image_out[i1][:copy_range] = np.average((np.roll(image_out, 1, axis=0)[i1][:copy_range], image_out[i1][:copy_range], np.roll(image_out, -1, axis=0)[i1][:copy_range]))
            image_out[i1][len(image_out[0])-copy_range:] = np.roll(image_out, 1, axis=0)[i1][len(image_out[0]) - copy_range:]

    return image_out

def get_avg_max_difference(image):
    '''
    :param image: np.array(rows, cols) of uint8 type
    :return: average absolute value of difference btw:  self cross correlation max AND
                                                        self cross correlation at cross correlation max
    '''
    avg_max_difference = 0
    cross_correlation = np.zeros((len(image), len(image[0])))
    self_cross_correlation = np.zeros((len(image), len(image[0])))

    for i in range(1, len(image)):
        cross_correlation[i] = get_cross_correlation(image, i)
        self_cross_correlation[i] = get_self_cross_correlation(image, i)
        avg_max_difference += np.abs(np.max(self_cross_correlation[i]) -
                                     self_cross_correlation[i][np.argmax(cross_correlation[i])]) / len(image)

    return avg_max_difference

def shift_image(image, threshold_lower, threshold_upper):

    image_out = np.copy(image)
    avg_max_difference = get_avg_max_difference(image_out)
    shifted_lines = 0

    for i in range(1, len(image_out)):
        cross_correlation_argmax = np.argmax(get_cross_correlation(image_out, i)).astype(int)
        self_cross_correlation = get_self_cross_correlation(image_out, i)
        max_difference = np.abs(self_cross_correlation[cross_correlation_argmax] -
                          np.max(self_cross_correlation))

        if (max_difference < threshold_upper) & (max_difference > threshold_lower):
            image_out[i] = np.roll(image_out[i], -cross_correlation_argmax)
            shifted_lines += 1

    print(shifted_lines)
    return image_out

def get_threshold(image):

    image_out = np.copy(image)
    max_difference = np.zeros(len(image_out))
    shifted_line = np.zeros(len(image_out), dtype=bool)
    avg_max_difference = 0.
    avg_avg_max_difference = 0.
    shifted_lines = 0

    for i in range(1, len(image_out)):

        cross_correlation = get_cross_correlation(image_out, i)
        self_cross_correlation = get_self_cross_correlation(image_out, i)

        difference = np.abs(cross_correlation - self_cross_correlation)
        avg_avg_max_difference += np.average(difference) / (len(difference))
        max_difference[i] = np.max(difference)

        if (np.argmax(cross_correlation) != 0):
            plt.plot(difference)
            image_out[i] = np.roll(image_out[i], -np.argmax(cross_correlation))
            shifted_lines += 1

    #plt.plot(np.arange(len(max_difference)), max_difference, 'r', np.arange(len(max_difference)), np.full((len(max_difference)), np.average(max_difference)), 'b', np.full((len(max_difference)), avg_avg_max_difference), 'y')
    plt.show()
    factor = np.sqrt(np.max(max_difference)/np.average(max_difference))

    return np.average(max_difference), factor

def cut_walls(image, pixels):

    image_out = np.copy(image)
    image_out = np.delete(image_out, np.s_[:pixels], 1)
    image_out = np.delete(image_out, np.s_[len(image_out[0])-pixels:], 1)

    return image_out


#fn = str(input("File : ")) # uncomment this to enable user interaction.
fn = "desync1.pgm"
im0 = misc.imread(fn)
im1 = np.copy(im0)
im2 = np.copy(im0)

rubbish = int(0.01*len(im0[0])/2)
print("rubbish: {0}".format(rubbish))

avg, factor = get_threshold(im0)

print(factor)

im2 = shift_image(im1, avg, 10*avg)

plt.subplot(121), plt.imshow(im0, cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(im2, cmap=plt.cm.gray)

plt.show()

im1 = clean_up(im2)

plt.subplot(121), plt.imshow(im0, cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(im1, cmap=plt.cm.gray)

plt.show()